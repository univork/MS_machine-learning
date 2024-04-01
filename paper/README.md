## Georgian real estate website scrapers

Orchestrated with luigi. Outputs multiple csv files one for each webiste and one with all website data combined.

Current websites:
- [ss.ge](https://home.ss.ge/ka/udzravi-qoneba)
- [myhome.ge](https://www.myhome.ge/ka/)

### How to run
```sh
pip install .

luigid &
python -m luigi --module scrapers.writer Writer
```
