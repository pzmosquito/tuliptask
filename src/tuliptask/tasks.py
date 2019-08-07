from .utils import TextUtil
from . import proc


class KubeTask:
    context = None
    namespace = None

    def setup(self, parser):
        """
        add --context and --namespace arguments to the parser.
        """
        parser.add_argument(
            "--context",
            help="Kubernetes context",
        )
        parser.add_argument(
            "--namespace",
            help="Kubernetes namespace",
        )

    
    def k(self, cmdstr, **kwargs):
        """
        run kubectl with --context and --namespace if provided.
        """
        extra = ""
        if self.context:
            extra += f" --context={self.context}"
        if self.namespace:
            extra += f" --namespace={self.namespace}"

        proc.k(f"{extra} {cmdstr}", **kwargs)
    
    def kube_info(self):
        ctx_str = f"current-context: {TextUtil.colored_text(self.context or '$(kubectl config current-context)')}"
        ns_str = f"namespace: {TextUtil.colored_text(self.namespace)}" if self.namespace else ""
        proc.run(f'echo "{ctx_str}\t{ns_str}\n"')

    def run(self, args):
        self.context = args.context
        self.namespace = args.namespace
