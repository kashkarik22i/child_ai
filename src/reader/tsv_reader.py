from __future__ import unicode_literals

import csv

class TSVReader:
  def __init__(self):
    self.clear_init()

  def clear_init(self):
    self.ids = []
    self.questions = {}
    self.correct_answers = {}
    self.answers = {}

  def read_file(self, filename):
    self.clear_init()
    with open(filename, 'rb') as f:
      areader = csv.reader(f, dialect='excel-tab')
      header = next(areader)
      assert(len(header)==7)
      for row in areader:
        self.ids.append(int(row[0]))
        self.questions[int(row[0])] = row[1]
        self.correct_answers[int(row[0])] = row[2]
        self.answers[int(row[0])] = [row[3], row[4], row[5], row[6]]

  def get_question(self, question_id):
    return self.questions[question_id]

  def get_answers(self, question_id):
    return self.answers[question_id]

  def get_correct_answer_letter(self, question_id):
    return self.correct_answers[question_id]
    
  def get_correct_answer_text(self, question_id):
    corr_letter = self.get_correct_answer_letter(question_id)
    if corr_letter=='A':
      return 0
    elif corr_letter=='B':
      return 1
    elif corr_letter=='C':
      return 2
    else:
      return 3

  def test(self):
    self.read_file('test_file.tsv')
    
    q = self.get_question(0)
    a = self.get_answers(0)
    cal = self.get_correct_answer_letter(0)
    cat = self.get_correct_answer_text(0)

    expected = ('question', 'C', 2, ['true', 'false', 'no idea', 'depends']) 
    actual = (q, cal, cat, a)

    if actual==expected:
      print 'test passed' 
    else:
      print 'test failed'
      print 'expected: ', expected
      print '  actual: ', actual
    

r = TSVReader()
r.test()

