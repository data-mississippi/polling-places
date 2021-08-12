# polling places
This ETL process extracts a single PDF that the Secretary of State's office released for the 2020 election. The PDF includes changes to some polling locations. Future versions of this will ideally include all the state's polling locations, by year.

## system requirements
- python 3.9
- make

## setup
in a virtual environment:
```python
pip install -r requirements.txt
```

configure aws credentials, [following their documentation](https://docs.aws.amazon.com/textract/latest/dg/setup-awscli-sdk.html)

## run
extract the polling place changes:
```bash
make all
```

clean up:
```bash
make clean
```
