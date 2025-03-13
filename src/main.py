import jinja2
from bs4 import BeautifulSoup
from glob import glob
from os import path
from urllib.parse import quote


dirname = path.dirname(__file__)
template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(path.join(dirname, "templates")),
    autoescape=jinja2.select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True
)


def main():
    paths = glob(path.join(dirname, "../.svg_exports/*.svg"))

    icons = dict()

    for file_path in paths:
        with open(file_path) as file:
            name = path.basename(file_path)[:-4]
            icons[name] = quote(str(Icon(file.read())))

    with open(path.join(dirname, "../output/icons.css"), "w") as file:
        file.write(template_env.get_template('icons.css').render(icons=icons))

    with open(path.join(dirname, "../output/index.html"), "w") as file:
        file.write(template_env.get_template('index.html').render(icons=icons))


class Icon:
    def __init__(self, txt):
        self.template = template_env.get_template('icon.svg')

        soup = BeautifulSoup(txt, 'lxml-xml')

        self.styles = dict([
            pair.split(":") for pair in soup
            .find("svg")
            .attrs["style"]
            .split(";") if pair != ''
        ])
        self.styles["stroke"] = "#ffffff"

        self.paths = [Path(str(path)) for path in soup.find_all("path")]

    def __str__(self):
        return self.template.render(styles=self.styles, paths=self.paths)


class Path:
    def __init__(self, txt):
        self.template = template_env.get_template('path.svg')

        soup = BeautifulSoup(txt, 'lxml-xml')
        self.path = soup.find("path").attrs["d"]
        self.styles = dict([
            pair.split(":") for pair in soup
            .find("path")
            .attrs["style"]
            .split(";") if pair != ''
        ])
        self.styles["stroke"] = "#ffffff"

    def __str__(self):
        return self.template.render(path=self.path, styles=self.styles)


if __name__ == '__main__':
    main()
