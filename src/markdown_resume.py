import click
import os
import subprocess
import yaml
import pystache
import uuid
import glob
from utils import swap_extension, replace_fa_strings

def output_pdf(input_file, output_file, contextfile):
    output_file = swap_extension(input_file.name, "pdf")
    print "RESUME: Writing PDF to ", output_file
    cmd = ['pandoc', '--standalone', '--template', contextfile.name,
         '--from', 'markdown', '--to', 'context', '-V', 'papersize=A4',
         '-o', 'resume_inter.tex', input_file.name]
    subprocess.call(cmd)
    subprocess.call(["context", "resume_inter.tex"])
    os.rename("resume_inter.pdf", output_file)
    for temp_file in glob.glob("resume_inter*"):
        os.remove(temp_file)


def output_html(input_file, output_file, stylesheet_file):

    print "RESUME: Writing HTML to ", output_file
    cmd = ['pandoc', '--standalone', '-H', stylesheet_file.name,
           '--from', 'markdown', '--to', 'html',
           '-o', output_file, input_file.name]
    subprocess.call(cmd)

    replace_fa_strings(output_file)

@click.command()
@click.argument('input_file', type=click.File('r'))
@click.option('--output', default="all", help="Output file formats "
    "select from 'html', 'pdf' or 'all' [default to 'all']")
@click.option('--stylesheet', default=None, help="Stylesheet to use "
    "for HTML output.  defaults to the Markdown file filename, with "
    "the extension .css", type=click.File('r'))
@click.option('--contextfile', default=None, help="ConTeXt file to use "
    "for PDF output.  defaults to the Markdown file filename, with "
    "the extension .tex", type=click.File('r'))
@click.option('--private_file', default=None, help="A YAML file containing "
    "any private information (e.g. telephone number) that you do not want "
    "to check into the repo.  If this is set, the code will parse out the "
    "YAML file and replace anything in {{double curly parens}} in the "
    "Markdown", type=click.File('r'))
@click.option('--keep-intermediate-file/--no-keep-intermediate-file',
              default=False, help="Keep the intermediate Markdown file with "
              "private info and FontAwesome fonts rendered in place [default "
              "to False]")
@click.option('-v', '--verbose', count=True, help="More verbose output")
def cli(input_file, output, stylesheet, contextfile, private_file,
        keep_intermediate_file, verbose):
    """Build resume from markdown file.  Will write files to the same
    place as the input Markdown file, just with different extensions.

    Required option is:

    INPUT_FILE:  Name of a markdown file containing your resume
    """

    intermediate_file = None

    # HTML output option parsing
    if output in ["html", "all"]:

        html_output_file = swap_extension(input_file.name, "html")

        if stylesheet is None:
            # If the stylesheet option is not set, then try to find one
            # in the same location as the resume file
            stylesheet_name = swap_extension(input_file.name, "css")
            try:
                stylesheet = open(stylesheet_name, "r")
                if verbose > 0:
                    print "RESUME: Opened stylesheet", stylesheet_name
            except IOError:
                raise IOError("RESUME: Failed to open CSS file",
                              stylesheet_name)

    if output in ["pdf", "all"]:
        pdf_output_file = swap_extension(input_file.name, "pdf")

        if contextfile is None:
            # If the stylesheet option is not set, then try to find one
            # in the same location as the resume file
            contextfile_name = swap_extension(input_file.name, "tex")
            try:
                contextfile = open(contextfile_name, "r")
                if verbose > 0:
                    print "RESUME: Opened contextfile", contextfile_name
            except IOError:
                raise IOError("RESUME: Failed to open Context file",
                              contextfile_name)

    if private_file is not None:
        # If there is a YAML file containing private info, add that
        # to the markdown
        if verbose > 0:
            print "RESUME: Inserting private info"
        private_info = yaml.load(private_file)
        renderer = pystache.Renderer()
        markdown_txt = input_file.read()

        intermediate_file = input_file.name + "." +  str(uuid.uuid1())
        with open(intermediate_file, "w") as f:
            f.write(pystache.render(
                markdown_txt, private_info).encode('utf-8'))
        if verbose > 1:
            print "RESUME: Storing temporary data to : ", intermediate_file
        input_file = open(intermediate_file, "r")

    # Generate the files
    if output in ["pdf", "all"]:
        output_pdf(input_file, pdf_output_file, contextfile)
    if output in ["html", "all"]:
        output_html(input_file, html_output_file, stylesheet)

    # Cleanup
    if intermediate_file is not None and not keep_intermediate_file:
        if verbose > 1:
            print "RESUME: Removing intermediate file : ", intermediate_file
        os.remove(intermediate_file)



if __name__ == "__main__":
    cli()
