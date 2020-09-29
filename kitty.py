#!/usr/bin/env python3

import os
import sys
import requests
import re
from html.parser import HTMLParser


def main():
    problem_name = str(sys.argv[1])
    create_directories(problem_name)
    problem_html = fetch_problem(problem_name)
    parse_testcases(problem_html, problem_name)
    copy_templates(problem_name)


def create_directories(problem_name):
    path = problem_name + "/tests"
    try:
        os.makedirs(path)
    except OSError:
        print("Creation of directory %s failed!" % path)

def fetch_problem(problem_name):
    problem_url = "https://open.kattis.com/problems/" + problem_name
    return requests.get(problem_url).text

def parse_testcases(problem_html, problem_name):
    class MyHTMLParser(HTMLParser):
        is_example = False
        is_input = False
        example_counter = 0
        example = []

        def handle_starttag(self, tag, attrs):
            if tag == "pre":
                self.is_input = not self.is_input
                self.is_example = True

        def handle_endtag(self, tag):
            if tag == "pre":
                self.is_example = False

        def handle_data(self, data):
            if self.is_example:
                # Is input example
                if self.is_input:
                    filename = problem_name + "/tests/input_" + str(self.example_counter) +".txt"
                    example_file = open(filename, "w+")
                    example_file.write(data)
                    example_file.close()

                else:
                    # Is output example
                    filename = problem_name + "/tests/output_" + str(self.example_counter) +".txt"
                    example_file = open(filename, "w+")
                    example_file.write(data)
                    example_file.close()
                    self.example_counter += self.example_counter + 1


    parser = MyHTMLParser()
    parser.feed(problem_html)

def copy_templates(problem_name):

    (makefile_template, maincpp_template) = populate_tempates(problem_name)
    
    # Create makefile from template
    makefile = open(problem_name + "/Makefile", "w+")
    makefile.write(makefile_template)
    makefile.close()

    # Create main.cpp from template
    maincpp = open(problem_name + "/main.cpp", "w+")
    maincpp.write(maincpp_template)
    maincpp.close()

def populate_tempates(problem_name):
    makefile_template = """
all: 
	${CXX} -o """ + problem_name +  """ main.cpp

run: all
	./""" + problem_name + """

"""

    maincpp_template = """
int main() {


    return 0;
}
"""
    return (makefile_template, maincpp_template)


if __name__ == "__main__":
    main()