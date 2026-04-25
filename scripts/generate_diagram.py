import os
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import ELB
from diagrams.aws.compute import EKS, ECR
from diagrams.aws.devtools import Codebuild
from diagrams.onprem.network import Nginx
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.ci import GithubActions
from diagrams.programming.framework import FastAPI
from diagrams.generic.compute import Rack

os.makedirs("docs", exist_ok=True)

graph_attr = {
    "bgcolor": "#0d1117",
    "fontcolor": "#e6edf3",
    "fontname": "Helvetica",
    "pad": "0.8",
    "splines": "ortho",
    "dpi": "150",
}
node_attr = {"fontcolor": "#e6edf3", "fontname": "Helvetica", "fontsize": "12"}
edge_attr = {
    "color": "#58a6ff",
    "fontcolor": "#8b949e",
    "fontname": "Helvetica",
    "fontsize": "10",
}

with Diagram(
    "mlops-serving-platform",
    filename="docs/architecture_diagram",
    outformat="png",
    graph_attr=graph_attr,
    node_attr=node_attr,
    edge_attr=edge_attr,
    show=False,
):
    with Cluster("Dev — Docker Compose", graph_attr={"bgcolor": "#1a1a2e", "fontcolor": "#e6edf3"}):
        internet = Rack("Internet")
        nginx_dev = Nginx("Nginx :80")
        api_dev = FastAPI("FastAPI :8000")
        model = Rack("Isolation Forest\nmodel.joblib")
        prom_dev = Prometheus("Prometheus :9090")

        internet >> nginx_dev >> api_dev >> model
        api_dev >> prom_dev

    with Cluster("Prod — Kubernetes / EKS", graph_attr={"bgcolor": "#1a2744", "fontcolor": "#e6edf3"}):
        elb = ELB("Load Balancer")
        svc = Rack("K8s Service")
        pod1 = FastAPI("Pod 1")
        pod2 = FastAPI("Pod 2")
        ecr = ECR("ECR")
        prom_prod = Prometheus("Prometheus")

        elb >> svc >> [pod1, pod2]
        ecr >> Edge(style="dashed") >> pod1
        ecr >> Edge(style="dashed") >> pod2
        prom_prod >> Edge(style="dashed", label="scrape /metrics") >> pod1
        prom_prod >> Edge(style="dashed", label="scrape /metrics") >> pod2

    with Cluster("CI/CD — GitHub Actions", graph_attr={"bgcolor": "#1a2e1a", "fontcolor": "#e6edf3"}):
        gh = GithubActions("GitHub Actions")
        build = Codebuild("test + build")
        ecr_ci = ECR("ECR")
        eks = EKS("EKS")

        gh >> build >> ecr_ci >> Edge(label="push image") >> eks
        eks >> Edge(label="kubectl apply", style="dashed") >> eks

print("Diagram generated: docs/architecture_diagram.png")
