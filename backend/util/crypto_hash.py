import hashlib
import json


def crypto_hash(*args):
    """
    Return a sha 256 hash of the given args.
    """
    string_args = sorted(map(json.dumps, args))
    joined_args = ''.join(string_args)
    return hashlib.sha256(joined_args.encode('utf-8')).hexdigest()

def main():
    print(f"crypto_hash('one',2,[3]): {crypto_hash('one',2,[3])}")
    print(f"crypto_hash(2,'one',[3]): {crypto_hash(2,'one',[3])}")


if __name__ == '__main__':
    main()