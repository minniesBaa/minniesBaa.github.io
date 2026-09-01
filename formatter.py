import regex as re

# r"<\S+[^\s.]*\.[^\s]*\/\S+[^>]+>"
# r"<[^\s:.>]*\.[^\s>]*[^>]+>"    matches urls with no protocol
# r"<localhost:[\d]+\s?[^>]+>"    matches localhost urls

def add_protocol(s):
    s = s.group(0)
    return f"<http://{s.strip("<")}" 

# r"<[^>\/]+\/[^>\/]+\/[^>\/]+\s?[^>]+>"

def expand_link(s):
    s = s.group(0)
    a, b, c = s.strip("<").strip(">").split("/", 2)
    c, _, d = c.partition(" ")
    if a.lower() == "github":
        return f"<https://github.com/{b}/{c} {d}>"

# r"<\S+:\/\/\S+[^\s.]*\.[^\s]*\/\S+[^>]+>"
# r"<\S+:\/\/\S+[^\s.]*\.[^>]+>"
# r"<\S+:\/\/\S+[^\s.]*[\.:][^>]+>"

# r"https?:\/\/github.com\/[^\/\s]+\/[^\/\s]+\/?"

def format_link(s: str):
    s = s.group(0) 
    s = s.strip("<").strip(">")
    url, _, disp = s.partition(" ")        
    
    if disp:
        disp = disp.replace("\\", r"\\").replace("]", r"\]").replace("[", r"\]")
    else: 
        if re.fullmatch(r"https?:\/\/github.com\/[^\/\s]+\/[^\/\s]+\/?", url.lower()): # match a github base repo url
            _, _, _, disp = url.split("/", 3)
        elif re.fullmatch(r"https?:\/\/github.com\/[^\/\s]+\/[^\/\s]+\/tree\/.+", url.lower()): # match a github tree path
            _, _, _, d1, d2, _, d3, d4 = url.split("/", 7)
            disp = f"{d1}/{d2} {d3} /{d4}"
        else:
            disp = url.replace("http://", "").replace("https://", "")
    
    return f"[{disp}]({url})"

with open("README.md", "r") as f:
    data = f.read()

data = re.sub(r"<[^>\/]+\/[^>\/]+\/[^>\/]+\s?[^>]+>", expand_link, data)
data = re.sub(r"<[^\s:.>]*\.[^\s>]*[^>]+>", add_protocol, data)
data = re.sub(r"<localhost:[\d]+\s?[^>]+>", add_protocol, data)
data = re.sub(r"<\S+:\/\/\S+[^\s.]*[\.:][^>]+>", format_link, data)

with open("README.md", "w") as f:
    f.write(data)