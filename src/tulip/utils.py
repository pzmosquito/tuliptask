from . import proc


class GitUtil:
    @staticmethod
    def git_ts():
        """
        get git timestamp
        """
        cmdstr = "git log -n 1 --no-notes --pretty=format:'%ai'"
        return proc.output(cmdstr)

    @staticmethod
    def git_hash():
        """
        get git hash
        """
        cmdstr = "git rev-parse HEAD"
        return proc.output(cmdstr)


class TextUtil:
    @staticmethod
    def colored_text(str, color=33):
        """
        format text with color
        """
        return f"\033[{color}m{str}\033[0m"

    @staticmethod
    def eval_file(file_path, vars_dict):
        """
        read and replace placeholder in the file (in ${} format) with given dict.
        """
        # open file
        file = open(file_path, "r")

        try:
            # replace ${key} with val
            content = file.read()
            for key, val in vars_dict.items():
                content = content.replace(f"${{{key}}}", str(val))
        finally:
            # close file
            file.close()

        return content