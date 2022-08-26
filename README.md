# Echargement.py

## Usage

```bash
./echargement.py --badge 123456789 --fullname "DOE John" --site-url https://www.e-chargement.com/api/libertis
```

It will save the result to balance.json

```json
{
    "2022-08-19": 6.82
}
```

You can change the file path with --save-path arg

```bash
./echargement.py --badge 123456789 --fullname "DOE John" --site-url https://www.e-chargement.com/api/libertis --save-path /tmp/my_balance.json
```
