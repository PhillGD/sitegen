class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html not implemented")
    
    def props_to_html(self):
        props_string = ""
        if self.props is not None:
            for prop in self.props:
                props_string += f" {prop}=\"{self.props[prop]}\""
        return props_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, Children: {self.children}, Props: {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, Props: {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Parent nodes must have a tag")
        if not self.children:
            raise ValueError("Parent nodes must have children")
        child_string = ""
        for child in self.children:
            child_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"
    
    def __repr__(self):
        print(self.children)
        return f"ParentNode({self.tag}, Children: {self.children}, Props: {self.props})"
        
        