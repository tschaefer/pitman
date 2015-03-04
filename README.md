# Pitman

Dig for your favored Podcast.

## Usage

```
$ pitman --help
usage: pitman [-h] [-p {Sleaze,Mobilee,Drumcode,RA,Systematic,CLR}]
              {show,search,get} ...

Dig for your favored Podcast.

positional arguments:
  {show,search,get}

optional arguments:
  -h, --help            show this help message and exit
  -p {Sleaze,Mobilee,Drumcode,RA,Systematic,CLR}, --podcast {Sleaze,Mobilee,Drumcode,RA,Systematic,CLR}
```

```
$ pitman show --help
usage: pitman show [-h] [-l LIMIT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        limit show to last N episodes
  -v, --verbose         verbose output
```

```
$ pitman search --help
usage: pitman search [-h] artist [artist ...]

positional arguments:
  artist      search for artist

optional arguments:
  -h, --help  show this help message and exit
```

```
$ pitman get --help
usage: pitman get [-h] episode [episode ...]

positional arguments:
  episode     download episode

optional arguments:
  -h, --help  show this help message and exit
```
