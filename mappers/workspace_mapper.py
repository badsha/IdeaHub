from api_models.workspace import Workspace as WorkspaceDTO

def map_workspace(domain_obj) -> WorkspaceDTO:
    # domain_obj may be a dict for now
    return WorkspaceDTO(**domain_obj)
