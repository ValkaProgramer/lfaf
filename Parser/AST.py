class ASTNode:
    def __init__(self, tuple):
        type, name = tuple
        self.type = type
        self.name = name
        self.children = []

class AST:
    def ast(self, tokens):
        root = ASTNode(("Code", "Block"))
        current_node = root
        new_node = ASTNode(tokens[0])
        current_node.children.append(new_node)
        current_node = new_node
        new_node = ASTNode(tokens[1])
        current_node.children.append(new_node)
        new_node = ASTNode(("Arguments", "Arguments"))
        current_node.children.append(new_node)
        new_node = ASTNode(tokens[len(tokens) - 2])
        current_node.children.append(new_node)
        current_node = current_node.children[1]
        for index in range(2, len(tokens) - 1):
            current_node.children.append(ASTNode(tokens[index]))

        return root