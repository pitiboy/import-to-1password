# KeePass/MacPass XML to 1Password CSV converter

Migrate your KeePass(X)/MacPass data to 1Password #: Export your KeePass(X)/MacPass data to XML,
use this script to convert it to a CSV, and then import the CSV into
1Password #.

## Prerequisites

Install dependencies:

- `pip install -r requirements.txt`

## Usage

- Export your KeePassX/MacPass passwords to `./input/passwords.xml`.
- Run `keepass or macpass script`.
  - That'd export the csv as `./output/passwords.csv`
  - I invoked `python macpass1p.py`
- Open *1Password* (preferrably Desktop app) and go to *File > Import > IMport a CSV file*
    - choose your input type (most probably *Login*)
    - choose your vault
    - pick `./output/passwords.csv`.

Benefits:
- If you had used *1 Password 7* Desktop, 
  - all of your imported files would be associated with a custom **tag**, based on the timestamp of importing. That *tag* you can rename to anything (using Desktop app, after right click on the *tag* under *TAGS* in the *left menu*). 
  
    This is very useful if you import your data in chunks so you can add custom tag exclusively for that import chunk.
- If you import Online,
  - you can customize the import configuration, with custom field mapping (not needed for standard *Login* type as this script uses the correct format)
  - there will be no *tag* associated

**Don't forget to delete** all the files under input/output, as using passwords in *plain text*!

## Documentation

- [1Password CSV Documentation](https://support.1password.com/#csv--comma-separated-values)

## License

This software is released under the [MIT License](http://opensource.org/licenses/MIT).
