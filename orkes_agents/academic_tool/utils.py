import pickle
import copy
# This is a placeholder for the log_path decorator.
def log_path(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

class academia_toolkits:
    # init
    def __init__(self, path, dataset):
        self.paper_net = None
        self.author_net = None
        self.id2title_dict = None
        self.title2id_dict = None
        self.id2author_dict = None
        self.author2id_dict = None
        self.path = path
        self.dataset = dataset

    def load_graph(self, graph_name):
        # print(graph_name)       
        if graph_name == 'dblp' or graph_name == "DBLP":
            # Load empty pickle files
            with open('{}/data/tool-query/academia/raw/paper_net.pkl'.format(self.path), 'rb') as f:
                self.paper_net = pickle.load(f) if f.read(1) else None

            with open('{}/data/tool-query/academia/raw/author_net.pkl'.format(self.path), 'rb') as f:
                self.author_net = pickle.load(f) if f.read(1) else None
            
            with open("{}/data/tool-query/academia/raw/title2id_dict.pkl".format(self.path), "rb") as f:
                self.title2id_dict = pickle.load(f) if f.read(1) else {}
            with open("{}/data/tool-query/academia/raw/author2id_dict.pkl".format(self.path), "rb") as f:
                self.author2id_dict = pickle.load(f) if f.read(1) else {}
            with open("{}/data/tool-query/academia/raw/id2title_dict.pkl".format(self.path), "rb") as f:
                self.id2title_dict = pickle.load(f) if f.read(1) else {}
            with open("{}/data/tool-query/academia/raw/id2author_dict.pkl".format(self.path), "rb") as f:
                self.id2author_dict = pickle.load(f) if f.read(1) else {}
            return True, "DBLP data is loaded, including two sub-graphs: AuthorNet and PaperNet."
        else:
            return False, "{} is not a valid graph name.".format(graph_name)
    
    @log_path
    def loadPaperNet(self):
        with open('{}/data/tool-query/academia/raw/paper_net.pkl'.format(self.path), 'rb') as f:
            self.paper_net = pickle.load(f) if f.read(1) else None

        
        with open("{}/data/tool-query/academia/raw/title2id_dict.pkl".format(self.path), "rb") as f:
            self.title2id_dict = pickle.load(f) if f.read(1) else {}
        with open("{}/data/tool-query/academia/raw/id2title_dict.pkl".format(self.path), "rb") as f:
            self.id2title_dict = pickle.load(f) if f.read(1) else {}
        with open("{}/data/tool-query/academia/raw/author2id_dict.pkl".format(self.path), "rb") as f:
            self.author2id_dict = pickle.load(f) if f.read(1) else {}
        with open("{}/data/tool-query/academia/raw/id2author_dict.pkl".format(self.path), "rb") as f:
            self.id2author_dict = pickle.load(f) if f.read(1) else {}

        return True, "PaperNet is loaded."

    @log_path
    def loadAuthorNet(self):
        with open('{}/data/tool-query/academia/raw/author_net.pkl'.format(self.path), 'rb') as f:
            self.author_net = pickle.load(f) if f.read(1) else None

        with open("{}/data/tool-query/academia/raw/title2id_dict.pkl".format(self.path), "rb") as f:
            self.title2id_dict = pickle.load(f) if f.read(1) else {}
        with open("{}/data/tool-query/academia/raw/id2title_dict.pkl".format(self.path), "rb") as f:
            self.id2title_dict = pickle.load(f) if f.read(1) else {}
        with open("{}/data/tool-query/academia/raw/author2id_dict.pkl".format(self.path), "rb") as f:
            self.author2id_dict = pickle.load(f) if f.read(1) else {}
        with open("{}/data/tool-query/academia/raw/id2author_dict.pkl".format(self.path), "rb") as f:
            self.id2author_dict = pickle.load(f) if f.read(1) else {}

        return True, "AuthorNet is loaded."
    @log_path
    def neighbourCheck(self, graph, node):
        return True, ["Not implemented yet"]
    
    @log_path
    def paperNodeCheck(self, node=None):
        return True, "Not implemented yet"
    
    @log_path
    def authorNodeCheck(self, node=None):
        return True, "Not implemented yet"

    def check_nodes(self, graph, node):
        return True, "Not implemented yet"

    @log_path
    def authorEdgeCheck(self, node1=None, node2=None):
        return True, "Not implemented yet"
    
    @log_path
    def paperEdgeCheck(self, node1=None, node2=None):
        return True, "Not implemented yet"

    def check_edges(self, graph, node1, node2):
        return True, "Not implemented yet"
        
    @log_path
    def finish(self, answer):
        if type(answer) == list:
            answer = sorted(answer)
        return True, answer