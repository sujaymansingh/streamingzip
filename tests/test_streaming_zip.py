import gzip
import io
import os
import shutil
import unittest
import streamingzip


class TestStreamingZip(unittest.TestCase):
    # There are two fixture files, lorem_ipsum.txt and lorem_ipsum.gz.
    # The latter is just the gzipped version of the former.
    # (Produced using the `gzip` command on OS X.)
    #
    # Testing is simply passing the contents of the files through our
    # gzipped and gunzipped functions!

    def expand_fixture_filename(self, fixture_name):
        test_base_dir = os.path.dirname(__file__)
        return os.path.join(test_base_dir, "fixtures", fixture_name)

    def test_gzipped(self):
        """Ensure that we can correctly gzip an input file.
        """
        our_zipped_file = io.BytesIO()

        # First we use our gzipped iterator to write to our_zipped_file...
        plaintext_filename = self.expand_fixture_filename("lorem_ipsum.txt")
        with open(plaintext_filename, "rb") as plaintext_file:
            shutil.copyfileobj(
                streamingzip.gzipped(plaintext_file),
                our_zipped_file,
            )
        our_zipped_file.seek(0)

        # We don't compare the contents of the zipped files, because they might
        # be different (gzip's file format includes timestamps).
        # So a simpler test is to unzip what we just zipped (using a known
        # unzipper!) and compare the plaintext we get.
        # So to test our zipped file is valid, we unzip it using the stdlib gzip.
        stdlib_unzipper = gzip.GzipFile(mode="rb", fileobj=our_zipped_file)
        unzipped_contents = stdlib_unzipper.read()

        # Now the unzipped contents should match the plaintext file!
        with open(plaintext_filename, "rb") as plaintext_file:
            self.assertEqual(plaintext_file.read(), unzipped_contents)

    def test_gunzipped(self):
        """Ensure that we can correctly gunzip an input file.
        """
        our_plaintext_file = io.BytesIO()

        zipped_filename = self.expand_fixture_filename("lorem_ipsum.gz")
        with open(zipped_filename, "rb") as zipped_file:
            shutil.copyfileobj(
                streamingzip.gunzipped(zipped_file),
                our_plaintext_file,
            )
        our_plaintext_file.seek(0)

        # Now the unzipped contents should match the plaintext file!
        plaintext_filename = self.expand_fixture_filename("lorem_ipsum.txt")
        with open(plaintext_filename, "rb") as plaintext_file:
            self.assertEqual(plaintext_file.read(), our_plaintext_file.getvalue())

    def test_reading_zero_bytes(self):
        plaintext_filename = self.expand_fixture_filename("lorem_ipsum.txt")
        with open(plaintext_filename, "rb") as plaintext_file:
            gzipped_file = streamingzip.gzipped(plaintext_file)
            self.assertEqual(gzipped_file.read(0), b"")

    def test_reading_all_bytes(self):
        plaintext_filename = self.expand_fixture_filename("lorem_ipsum.txt")
        with open(plaintext_filename, "rb") as plaintext_file:
            gzipped_file = streamingzip.gzipped(plaintext_file)

            # This should read all the bytes.
            gzipped_file.read()

            # So now we have nothing left.
            self.assertEqual(gzipped_file.read(0), b"")


if __name__ == "__main__":
    unittest.main()
