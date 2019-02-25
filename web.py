from sys import exit
from time import time, sleep
import requests
# import re
import mechanize

login_url = "http://35.167.100.168:3000/login"
download_url = "http://35.167.100.168:3000/submit/{}/download"
upload_url = "http://35.167.100.168:3000/submit/{}"

def save_response(b, f_name="graph", f_type="json"):
    html = open(f_name + '.' + f_type, 'w')
    html.write(b.response().read().decode("utf-8"))

def logged_in_browser():
    b = mechanize.Browser()
    b.set_handle_robots(False)

    b.open(login_url)
    b.select_form(action="/login")
    b.form["username"] = "Animaniacs"
    b.form["password"] = "2d82b0t8"
    print(b.form)
    print()
    # control = b.form.find_control("username")
    # print(control.type)
    # print()
    b.submit()


    return b

def download(graph_label="2.5.1"):
    b = logged_in_browser()
    # b.follow_link(nr=0)
    # b.follow_link(url="/submit/" + graph_label)
    b.retrieve(download_url.format(graph_label), "graph.json")

# def upload(b, seeds_file="seeds.txt", graph_label="2.5.1"):
#     b.open(upload_url.format(graph_label))
#
#     b.select_form(action="{}/upload".format(graph_label))
#     print(b.form)
#     print()
#     # print(b.method)
#     control = b.form.find_control(type="file")
#     # print(control.type)
#     # print(control.get_value(type="file"))
#     control.add_file(open(seeds_file, 'r'), None, "seeds.txt")
#     sleep(2)
#     # print(control)
#     print()
#     print(b.form)
#     print()
#
#     b.select_form(action="{}/upload".format(graph_label))
#     print(b.form)
#     print()
#
#     b.form.find_control(type="file").add_file(open(seeds_file, 'rb'), None, "seeds.txt")
#     print(b.form)
#     print()
#     b.submit()
#
#     b.form['hidden'] = "/Users/tkrasnoperov/Documents/Academics/CS144/pandemaniac/" + seeds_file
#     b.submit()
#     print(b.response().read())
#
if __name__ == "__main__":
    # graph_label = "2.10.10"
    # n_players, n_seeds, graph_id = [int(val) for val in graph_label.split(".")]
    download()
#
#     seeds_file = "seeds.txt"
#     with open(seeds_file, 'w') as f:
#         for i in range(50 * n_seeds):
#             f.write("1\n".format(i))
#
#     # start = time()
#     b = logged_in_browser()
    # download(graph_label=graph_label)
#     upload(b, seeds_file=seeds_file, graph_label=graph_label)
#     # print("time:", time() - start)
