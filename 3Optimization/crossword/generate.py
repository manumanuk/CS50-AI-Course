import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        self.total = 0

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        #for var in self.domains:
            #print(self.domains[var])
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.crossword.variables:
            for word in self.domains[variable].copy():
                if len(word) != variable.length:
                    self.domains[variable].remove(word)  
        return        
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return False
        #print("the " + str(overlap[0]+1) + "th character of var " + str(x.length) + " and the " + str(overlap[1]+1) + "th character of var " + str(y.length) + " must match")
        altered = False

        for xWord in self.domains[x].copy():
            notConsistent = True
            for yWord in self.domains[y].copy():
                match = False
                try:
                    match = (xWord[overlap[0]] == yWord[overlap[1]])
                except IndexError as e:
                    pass
                if match:
                    notConsistent = False
                    #print(xWord + " is consistent with " + yWord)
                    break
            if notConsistent:
                self.domains[x].remove(xWord)
                altered = True

        return altered

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = set()
        iterative = self.crossword.variables if arcs == None else arcs
        for var in iterative:
            for neighbour in self.crossword.neighbors(var):
                queue.add((var, neighbour))
        
        while len(queue) != 0:
            x, y = queue.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbour in self.crossword.neighbors(x):
                    if neighbour != y:
                        queue.add((neighbour, x))
        return True
            

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        variables = self.crossword.variables.copy()
        for variable in variables.copy():
            if variable in assignment and assignment[variable] != "":
                variables.remove(variable)
        
        if len(variables) == 0:
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        valuesToCheck = list(assignment.values())
        for x in self.crossword.variables:
            for y in self.crossword.variables:
                if x in assignment and y in assignment and x!=y:
                    overlap = self.crossword.overlaps[x, y]
                    if overlap != None and assignment[x][overlap[0]] != assignment[y][overlap[1]]:
                        return False
        for var in assignment:
            if var.length != len(assignment[var]):
                return False
            valuesToCheck.remove(assignment[var])
            if assignment[var] in valuesToCheck:
                return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        ruledOut = { word: 0 for word in self.domains[var] }
        for neighbor in self.crossword.neighbors(var):
            if neighbor in assignment.keys() and assignment[neighbor] != "":
                continue
            overlap = self.crossword.overlaps[var, neighbor]
            if overlap == None:
                continue
            for xWord in ruledOut:
                for yWord in self.domains[neighbor]:
                    if xWord[overlap[0]] != yWord[overlap[1]]:
                        ruledOut[xWord] += 1
        return sorted(list(ruledOut.keys()), key=ruledOut.__getitem__)
            
                        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        possibleVars = self.crossword.variables.copy()
        bestVars = dict()
        for variable in assignment:
            possibleVars.remove(variable)
        lowestVal = 0
        for var in possibleVars:
            domainSize = len(self.domains[var])
            if lowestVal == 0 or domainSize < lowestVal:
                lowestVal = domainSize
                bestVars = dict()
                bestVars[var] = len(self.crossword.neighbors(var))
            elif domainSize == lowestVal:
                bestVars[var] = len(self.crossword.neighbors(var))
        
        return sorted(bestVars.keys(), key=bestVars.__getitem__)[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment) and self.consistent(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                ac3Input = list()
                for var in self.domains:
                    if var not in assignment:
                        ac3Input.append(var)
                infer = self.ac3(ac3Input)
                if infer == False:
                    return None
                elif self.assignment_complete(assignment) and self.consistent(assignment):
                    return assignment
                result = self.backtrack(assignment)
                if result != None:
                    return assignment
        
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
