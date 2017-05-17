import sys

import streamingzip


if __name__ == "__main__":
    streamingzip.run_main(sys.argv[1], sys.stdin.buffer, sys.stdout.buffer)
