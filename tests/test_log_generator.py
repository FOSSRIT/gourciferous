import os

class TestLogGenerator(object):

    def test_compile_commits(self):
        from log_generator import compile_commits
        commits = compile_commits(os.getcwd())
        sorted_commits = [commits[x] for x in sorted(commits)]
        split = sorted_commits[0][0].split('|')
        assert split[0] == '1370448542', split[0]
        assert split[1] == 'Remy Decausemaker', split[1]
