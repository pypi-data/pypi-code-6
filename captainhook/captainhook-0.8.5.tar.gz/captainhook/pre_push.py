
def main():
    pass

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('remote_name')
    parser.add_argument('url')

    args = parser.parse_args()
    main(args.remote_name, args.url)
