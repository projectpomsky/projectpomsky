import time

import requests


def commit(commit_msg='Timeline', tag_name='2021.12.21_16.52'):
    import subprocess


    cmd = "pwd"
    res_pwd = subprocess.run(cmd.split(), capture_output=True, text=True).stdout

    cmd = "bash ./git_process_next_commit.sh {commit_msg} {tag}".format(commit_msg=commit_msg, tag=tag_name)
    res_bash = subprocess.run(cmd.split(), capture_output=True, text=True).stdout

    cmd = "git push"
    res_add = subprocess.run(cmd.split(), capture_output=True, text=True).stdout

    # cmd = "git commit -m \"{msg}\"".format(msg='test automated commit v2')
    # res_commit = subprocess.run(cmd.split(), capture_output=True, text=True).stdout
    #
    # cmd = "git tag \"{tag}\"".format(tag=tag_name)
    # res_tag = subprocess.run(cmd.split(), capture_output=True, text=True).stdout
    #
    # cmd = "git status"
    # res_status = subprocess.run(cmd.split(), capture_output=True, text=True).stdout
    #
    # cmd = "git push"
    # res_push = subprocess.run(cmd.split(), capture_output=True, text=True).stdout

    # cmd = "git add . && git commit -am \"{commit_msg}\" && git tag {tag} && git status".format(commit_msg='test automated commit',
    #                                                                              tag=tag_name)
    # res = subprocess.run(cmd.split(), capture_output=True, text=True).stdout

    # print(res)

#     if res_bash != '''On branch main
# Your branch is up to date with \'origin/main\'
#
# nothing to commit, working tree clean
# ''':
#         try:
#             resp = requests.post("https://api.github.com/repos/projectpomsky/projectpomsky-history/releases", json={
#                 "tag_name": tag_name,
#                 "owner": "projectpomsky",
#                 "repo": "projectspomsky-history",
#                 "generate_release_notes": True
#             }, headers={
#                 "Accept": "application/vnd.github.v3+json",
#                 "Authorization": "Basic cHJvamVjdHBvbXNreTpnaHBfWEptQkFUeUJXTXJQTmNWOFk3Mjg0YjBTcTh6dXBXMnQ4ek5I"
#             })
#
#             resp.raise_for_status()
#         except Exception as ex:
#             pass

    # bashCommand = "git status"
    # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate()
    #
    # cmd = "git add . && git commit -am \"{commit_msg}\" && git tag {tag}".format(commit_msg='', tag='')
    # res = subprocess.run(cmd.split(), capture_output=True, text=True).stdout
    # # 'total 0\n-rw-r--r--  1 memyself  staff  0 Mar 14 11:04 files\n'
    # print(res)

    #  curl \
    #   -X POST \
    #   -H "Accept: application/vnd.github.v3+json" \
    #   https://api.github.com/repos/octocat/hello-world/releases \
    #   -d '{"tag_name":"tag_name"}'

if __name__ == '__main__':
    try:
        commit()
    except Exception as e:
        print(str(e))