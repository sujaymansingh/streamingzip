## What is this?

If we have a python plaintext file, then we can wrap it in `gzipped`.

```
zipped_file = streamingzip.gzipped(input_file)
```

Now, whenever we read from `zipped_file`, it will read plaintext from `input_file`, compress the bytes and return them.

```
compressed_bytes = zipped_file.read(1024)
```

We can keep doing that until `input_file` is exhausted (in which case `zipped_file.read(size)` will return `b""`.


## Basic Usage

Python3 only! We deal in bytes.

- To gzip a file

```
with open(input_plaintext_filename, "rb") as input_file:
    gzipper = streamingzip.gzipped(input_file)

    # Now when we read from gzipper, it will internally read from input_file, compress
    # and return the result.
    # It uses an internal buffer so that the entire thing doesn't need to be loaded into
    # memory.
    with open(output_filename, "wb") as output_file:
        shutil.copyfileobj(gzipper, output_file)
```

- To gunzip    

```
with open(input_gzipped_filename, "rb") as input_file:
    gunzipper = streamingzip.gunzipped(input_file)

    with open(output_filename, "wb") as output_file:
        shutil.copyfileobj(gunzipper, output_file)
```


## Why do I want this?

Most of the time you can gzip a file in python 'on-the-fly'. I.e. without loading the entire
contents into memory or onto disk.

```
with open(input_plaintext_filename, "rb") as input_file:
    with open(output_gzipped_filename, "wb") as output_file:
        gzip_writer = gzip.GzipFile(mode="wb", fileobj=output_file)
        shutil.copyfileobj(input_file, gzip_writer)
```

This is great! But sometimes, you don't have direct access to the `output_file` object.
I.e. you have to provide an `input_file` that a function will use internally to write to
its `output_file`.

E.g. when uploading a file using [boto/boto3], you supply a `Fileobj` as input:
https://github.com/boto/boto3/blob/1.4.4/boto3/s3/inject.py#L373

In this case, the above example doesn't work as we don't have an `output_file` to write to.
So it is useful in this scenario to wrap the plaintext `input_file` in a wrapper that will
gzip the content.

```
zipped_input = streamingzip.gzipped(plaintext_input_file)
```

Here, whenever `read(n)` is called on `zipped_input`, it will read from `plaintext_input_file`,
compress and return `n` compressed bytes.

This way, you can pass in `zipped_input` to the function that requires a `input_file`, and
the gzipped data will be used. (And all this is done without reading the entire file into memory.)

For completeness, an `gunzipped` function is also provided.
