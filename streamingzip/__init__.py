import gzip
import shutil


def gzipped(input_file, *args, **kwargs):
    return StreamingZipFile(input_file, *args, **kwargs)


def gunzipped(input_file, *args, **kwargs):
    return gzip.GzipFile(fileobj=input_file, mode="rb")


class StreamingZipFile():
    """This 'wraps' around an input file, zipping it automatically as bytes are read.
    """
    def __init__(self, input_file, compresslevel=9, read_buffer_size=2 ** 20):
        self.input_file = input_file
        self.still_reading_input = True
        self.default_read_buffer_size = read_buffer_size

        self.byte_buffer = BytesBuffer()
        self.zipper = gzip.GzipFile(
            fileobj=self.byte_buffer,
            mode="wb",
            compresslevel=compresslevel
        )

    def read(self, size=-1):
        """Read from the input file, zip the bytes read, and return the zipped bytes.
        """
        if size == 0:
            return b""

        # size indicates how many zipped bytes we should return.
        # We need to decide how many plaintext bytes we read from our input.
        if size < 0:
            # This indicates that the caller wants the entire file!
            # Setting read_buffer_size to -1 will cause us to read the entire
            # file into memory.
            read_buffer_size = -1
        else:
            read_buffer_size = self.default_read_buffer_size

        while self.still_reading_input and len(self.byte_buffer) < size:

            plain_bytes = self.input_file.read(read_buffer_size)

            if plain_bytes == b"":
                self.still_reading_input = False
                self.zipper.close()
                break

            self.zipper.write(plain_bytes)

        # We have a big enough buffer (or we've finished reading the input file!)
        # Either way, we should be returning some bytes to whatever is consuming this.

        if len(self.byte_buffer) > size:
            result = self.byte_buffer.take_bytes(size)
        else:
            result = self.byte_buffer.take_all_bytes()

        return result


class BytesBuffer():
    def __init__(self):
        self.buffer_ = bytearray()

    def write(self, data):
        """Write data (which must be bytes!) to the end of our current buffer.
        """
        self.buffer_.extend(data)

    def take_bytes(self, num_bytes):
        """Remove and return num_bytes from the beginning of the current buffer.
        """
        if len(self.buffer_) == 0:
            return b""
        result = self.buffer_[:num_bytes]
        self.buffer_ = self.buffer_[num_bytes:]
        return result

    def take_all_bytes(self):
        """Remove all bytes from the current buffer
        """
        result = self.buffer_
        self.buffer_ = bytearray()
        return result

    def __len__(self):
        return len(self.buffer_)


def run_main(command, input_file, output_file):
    if command == "zip":
        shutil.copyfileobj(gzipped(input_file), output_file)
    elif command == "unzip":
        shutil.copyfileobj(gunzipped(input_file), output_file)
