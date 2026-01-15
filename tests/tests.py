import unittest
from pddlval import validate
import os
import glob

FILE_DIR = os.path.dirname(__file__)
DOMAIN_DIR = os.path.join(FILE_DIR, "domains")
PROBLEM_DIR = os.path.join(FILE_DIR, "problems")
PLAN_DIR = os.path.join(FILE_DIR, "plans")

class TestPDDLValidation(unittest.TestCase):
    def path_and_content(self, path):
        yield path
        with open(path, "r") as f:
            yield f.read()

    def test_domains(self):
        for valid_domain in glob.glob(os.path.join(DOMAIN_DIR, "valid*.pddl")):
            for domain in self.path_and_content(valid_domain):
                with self.subTest(domain=valid_domain):
                    self.assertTrue(validate(domain))

        for invalid_domain in glob.glob(os.path.join(DOMAIN_DIR, "invalid*.pddl")):
            for domain in self.path_and_content(invalid_domain):
                with self.subTest(domain=invalid_domain):
                    self.assertFalse(validate(domain))
    
    def test_problems(self):
        for valid_domain in glob.glob(os.path.join(DOMAIN_DIR, "valid*.pddl")):
            for domain in self.path_and_content(valid_domain):

                for valid_problem in glob.glob(os.path.join(PROBLEM_DIR, "valid*.pddl")):
                    for problem in self.path_and_content(valid_problem):
                        with self.subTest(problem=valid_problem):
                            self.assertTrue(validate(domain, problem))

                for invalid_problem in glob.glob(os.path.join(PROBLEM_DIR, "invalid*.pddl")):
                    for problem in self.path_and_content(invalid_problem):
                        with self.subTest(problem=invalid_problem):
                            self.assertFalse(validate(domain, problem))
    
    def test_plans(self):
        with open(os.path.join(DOMAIN_DIR, "valid.pddl")) as f:
            valid_domain = f.read()
        with open(os.path.join(PROBLEM_DIR, "valid.pddl")) as f:
            valid_problem = f.read()

        for valid_domain in glob.glob(os.path.join(DOMAIN_DIR, "valid*.pddl")):
            for domain in self.path_and_content(valid_domain):
                for valid_problem in glob.glob(os.path.join(PROBLEM_DIR, "valid*.pddl")):
                    for problem in self.path_and_content(valid_problem):                      
                          
                        for valid_plan in glob.glob(os.path.join(PLAN_DIR, "valid*.txt")):
                            for plan in self.path_and_content(valid_plan):
                                with self.subTest(plan=valid_plan):
                                    self.assertTrue(validate(domain, problem, plan))

                        for invalid_plan in glob.glob(os.path.join(PLAN_DIR, "invalid*.txt")):
                            for plan in self.path_and_content(invalid_plan):
                                with self.subTest(plan=invalid_plan):
                                    self.assertFalse(validate(domain, problem, plan))

if __name__ == "__main__":
    unittest.main()