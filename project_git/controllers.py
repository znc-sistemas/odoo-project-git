# -*- coding: utf-8 -*-
import datetime
import json
import re

from openerp import http, SUPERUSER_ID


def timestamp_from_utc(utc_str):
    fmt = "%Y-%m-%d %H:%M:%S"
    utc_str = utc_str.split('+')[0]
    return datetime.datetime.strptime(utc_str, fmt)


class ProjectGit(http.Controller):

    @http.route('/project_git/push/', auth='none')
    def push(self, **kw):
        """
        Receives git repositories push hooks

        For Bitbucket:
        https://confluence.atlassian.com/display/BITBUCKET/POST+hook+management

        Example payload:

        {
            "canon_url": "https://bitbucket.org",
            "commits": [
                {
                    "author": "marcus",
                    "branch": "master",
                    "files": [
                        {
                            "file": "somefile.py",
                            "type": "modified"
                        }
                    ],
                    "message": "Added some more things to somefile.py\n",
                    "node": "620ade18607a",
                    "parents": [
                        "702c70160afc"
                    ],
                    "raw_author": "Marcus Bertrand <marcus@somedomain.com>",
                    "raw_node": "620ade18607ac42d872b568bb92acaa9a28620e9",
                    "revision": null,
                    "size": -1,
                    "timestamp": "2012-05-30 05:58:56",
                    "utctimestamp": "2012-05-30 03:58:56+00:00"
                }
            ],
            "repository": {
                "absolute_url": "/marcus/project-x/",
                "fork": false,
                "is_private": true,
                "name": "Project X",
                "owner": "marcus",
                "scm": "git",
                "slug": "project-x",
                "website": "https://atlassian.com/"
            },
            "user": "marcus"
        }

        For Github:

        https://developer.github.com/v3/activity/events/types/#pushevent

        {
          "ref": "refs/heads/gh-pages",
          "before": "4d2ab4e76d0d405d17d1a0f2b8a6071394e3ab40",
          "after": "7700ca29dd050d9adacc0803f866d9b539513535",
          "created": false,
          "deleted": false,
          "forced": false,
          "base_ref": null,
          "compare": "https://github.com/baxterthehacker/public-repo/compare/4d2ab4e76d0d...7700ca29dd05",
          "commits": [
            {
              "id": "7700ca29dd050d9adacc0803f866d9b539513535",
              "distinct": true,
              "message": "Trigger pages build",
              "timestamp": "2014-10-09T17:10:36-07:00",
              "url": "https://github.com/baxterthehacker/public-repo/commit/7700ca29dd050d9adacc0803f866d9b539513535",
              "author": {
                "name": "Kyle Daigle",
                "email": "kyle.daigle@github.com",
                "username": "kdaigle"
              },
              "committer": {
                "name": "Kyle Daigle",
                "email": "kyle.daigle@github.com",
                "username": "kdaigle"
              },
              "added": [

              ],
              "removed": [

              ],
              "modified": [
                "index.html"
              ]
            }
          ],
          "head_commit": {
            "id": "7700ca29dd050d9adacc0803f866d9b539513535",
            "distinct": true,
            "message": "Trigger pages build",
            "timestamp": "2014-10-09T17:10:36-07:00",
            "url": "https://github.com/baxterthehacker/public-repo/commit/7700ca29dd050d9adacc0803f866d9b539513535",
            "author": {
              "name": "Kyle Daigle",
              "email": "kyle.daigle@github.com",
              "username": "kdaigle"
            },
            "committer": {
              "name": "Kyle Daigle",
              "email": "kyle.daigle@github.com",
              "username": "kdaigle"
            },
            "added": [

            ],
            "removed": [

            ],
            "modified": [
              "index.html"
            ]
          },
          "repository": {
            "id": 20000106,
            "name": "public-repo",
            "full_name": "baxterthehacker/public-repo",
            "owner": {
              "name": "baxterthehacker",
              "email": "baxterthehacker@users.noreply.github.com"
            },
            "private": false,
            "html_url": "https://github.com/baxterthehacker/public-repo",
            "description": "",
            "fork": false,
            "url": "https://github.com/baxterthehacker/public-repo",
            "forks_url": "https://api.github.com/repos/baxterthehacker/public-repo/forks",
            "keys_url": "https://api.github.com/repos/baxterthehacker/public-repo/keys{/key_id}",
            "collaborators_url": "https://api.github.com/repos/baxterthehacker/public-repo/collaborators{/collaborator}",
            "teams_url": "https://api.github.com/repos/baxterthehacker/public-repo/teams",
            "hooks_url": "https://api.github.com/repos/baxterthehacker/public-repo/hooks",
            "issue_events_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/events{/number}",
            "events_url": "https://api.github.com/repos/baxterthehacker/public-repo/events",
            "assignees_url": "https://api.github.com/repos/baxterthehacker/public-repo/assignees{/user}",
            "branches_url": "https://api.github.com/repos/baxterthehacker/public-repo/branches{/branch}",
            "tags_url": "https://api.github.com/repos/baxterthehacker/public-repo/tags",
            "blobs_url": "https://api.github.com/repos/baxterthehacker/public-repo/git/blobs{/sha}",
            "git_tags_url": "https://api.github.com/repos/baxterthehacker/public-repo/git/tags{/sha}",
            "git_refs_url": "https://api.github.com/repos/baxterthehacker/public-repo/git/refs{/sha}",
            "trees_url": "https://api.github.com/repos/baxterthehacker/public-repo/git/trees{/sha}",
            "statuses_url": "https://api.github.com/repos/baxterthehacker/public-repo/statuses/{sha}",
            "languages_url": "https://api.github.com/repos/baxterthehacker/public-repo/languages",
            "stargazers_url": "https://api.github.com/repos/baxterthehacker/public-repo/stargazers",
            "contributors_url": "https://api.github.com/repos/baxterthehacker/public-repo/contributors",
            "subscribers_url": "https://api.github.com/repos/baxterthehacker/public-repo/subscribers",
            "subscription_url": "https://api.github.com/repos/baxterthehacker/public-repo/subscription",
            "commits_url": "https://api.github.com/repos/baxterthehacker/public-repo/commits{/sha}",
            "git_commits_url": "https://api.github.com/repos/baxterthehacker/public-repo/git/commits{/sha}",
            "comments_url": "https://api.github.com/repos/baxterthehacker/public-repo/comments{/number}",
            "issue_comment_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/comments/{number}",
            "contents_url": "https://api.github.com/repos/baxterthehacker/public-repo/contents/{+path}",
            "compare_url": "https://api.github.com/repos/baxterthehacker/public-repo/compare/{base}...{head}",
            "merges_url": "https://api.github.com/repos/baxterthehacker/public-repo/merges",
            "archive_url": "https://api.github.com/repos/baxterthehacker/public-repo/{archive_format}{/ref}",
            "downloads_url": "https://api.github.com/repos/baxterthehacker/public-repo/downloads",
            "issues_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues{/number}",
            "pulls_url": "https://api.github.com/repos/baxterthehacker/public-repo/pulls{/number}",
            "milestones_url": "https://api.github.com/repos/baxterthehacker/public-repo/milestones{/number}",
            "notifications_url": "https://api.github.com/repos/baxterthehacker/public-repo/notifications{?since,all,participating}",
            "labels_url": "https://api.github.com/repos/baxterthehacker/public-repo/labels{/name}",
            "releases_url": "https://api.github.com/repos/baxterthehacker/public-repo/releases{/id}",
            "created_at": 1400625583,
            "updated_at": "2014-07-25T16:37:51Z",
            "pushed_at": 1412899789,
            "git_url": "git://github.com/baxterthehacker/public-repo.git",
            "ssh_url": "git@github.com:baxterthehacker/public-repo.git",
            "clone_url": "https://github.com/baxterthehacker/public-repo.git",
            "svn_url": "https://github.com/baxterthehacker/public-repo",
            "homepage": null,
            "size": 665,
            "stargazers_count": 0,
            "watchers_count": 0,
            "language": null,
            "has_issues": true,
            "has_downloads": true,
            "has_wiki": true,
            "has_pages": true,
            "forks_count": 0,
            "mirror_url": null,
            "open_issues_count": 24,
            "forks": 0,
            "open_issues": 24,
            "watchers": 0,
            "default_branch": "master",
            "stargazers": 0,
            "master_branch": "master"
          },
          "pusher": {
            "name": "baxterthehacker",
            "email": "baxterthehacker@users.noreply.github.com"
          },
          "sender": {
            "login": "baxterthehacker",
            "id": 6752317,
            "avatar_url": "https://avatars.githubusercontent.com/u/6752317?v=2",
            "gravatar_id": "",
            "url": "https://api.github.com/users/baxterthehacker",
            "html_url": "https://github.com/baxterthehacker",
            "followers_url": "https://api.github.com/users/baxterthehacker/followers",
            "following_url": "https://api.github.com/users/baxterthehacker/following{/other_user}",
            "gists_url": "https://api.github.com/users/baxterthehacker/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/baxterthehacker/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/baxterthehacker/subscriptions",
            "organizations_url": "https://api.github.com/users/baxterthehacker/orgs",
            "repos_url": "https://api.github.com/users/baxterthehacker/repos",
            "events_url": "https://api.github.com/users/baxterthehacker/events{/privacy}",
            "received_events_url": "https://api.github.com/users/baxterthehacker/received_events",
            "type": "User",
            "site_admin": false
          }
        }
        """

        http.request.uid = SUPERUSER_ID

        if 'payload' in http.request.params:
            payload_obj = json.loads(http.request.params['payload'])
            git_user = payload_obj['user']
            repo_url = '%s%s' % (
                payload_obj['canon_url'],
                payload_obj['repository']['absolute_url']
            )

            for commit in payload_obj['commits']:

                odoo_user = http.request.env['res.users'].search([["git_username", "=", commit['author']]])

                cm_message = commit['message']
                # TODO: use python-dateutil,
                # discover how to install python deps
                # convert timezone, remove hardcoded UTC-3
                cm_timestamp = timestamp_from_utc(commit['utctimestamp']) - datetime.timedelta(hours=3)

                # Extracts task ID from commit message
                ids = re.findall(r'\#\d+', cm_message)

                for task_id in [i.replace('#', '') for i in ids]:
                    project = http.request.env['project.task'].search(
                        [["id", "=", task_id]],
                    )

                    if project:
                        name = '%s\n\n%s%s' % (
                            cm_message,
                            repo_url,
                            '/'.join(['commits', commit['node']])
                        )

                        vals = {
                            'name': name,
                            'date': str(cm_timestamp),
                            # for the old API, used in project_timesheet
                            # task_id needs to be an integer, for new API
                            # it can be a string
                            'task_id': int(task_id),
                            # TODO: extract user ID from
                            # commit message and custom field
                            'user_id': SUPERUSER_ID,
                            'hours': 0.0
                        }

                        # Extracts time spent
                        time_match = re.search(r'T\d{1,2}:\d{1,2}', cm_message)
                        if time_match:
                            hours_tag = time_match.group()[1:]
                            h, m = hours_tag.split(':')
                            hours = int(h) + (int(m) / 60.0)
                            vals['hours'] = hours

                        work = http.request.env['project.task.work'].create(vals)
                        http.request.env['project.task.work'].write(work)

        return "OK"
