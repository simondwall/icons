# CSS Icon Library

## Development

```sh
watchexec -w .svg_exports -r -e py,css,html,svg -i 'output/*' -- 'python3 src/main.py && python3 -m http.server -d output'
```
