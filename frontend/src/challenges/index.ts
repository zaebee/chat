export interface ChallengeContent {
  title: string
  description: string
  testCode: string
  successMessage: string
}

export interface Challenge {
  id: string
  content: {
    [key: string]: ChallengeContent
  }
  startingCode: string
}

export const challenges: Challenge[] = [
  {
    id: '1',
    content: {
      en: {
        title: 'Add Two Numbers',
        description:
          'Write a Python function called `add` that takes two numbers as arguments and returns their sum.',
        testCode: [
          'import sys',
          'def run_tests():',
          '    test_cases = [',
          '        ((2, 3), 5),',
          '        ((-1, 1), 0),',
          '        ((10, -5), 5),',
          '    ]',
          '    all_passed = True',
          '    for i, (args, expected) in enumerate(test_cases):',
          '        try:',
          '            result = add(*args)',
          '            assert result == expected, f"Test #{i+1} failed for input {args}: returned {result}, expected {expected}"',
          '            print(f"Test #{i+1} passed!")',
          '        except Exception as e:',
          '            print(f"An error occurred: {e}", file=sys.stderr)',
          '            all_passed = False',
          '            break',
          '    if all_passed:',
          '        print("All tests passed!")',
          'run_tests()',
        ].join('\n'),
        successMessage: 'All tests passed!',
      },
      ru: {
        title: 'Сложить два числа',
        description:
          'Напишите функцию на Python с именем `add`, которая принимает два числа в качестве аргументов и возвращает их сумму.',
        testCode: [
          'import sys',
          'def run_tests():',
          '    test_cases = [',
          '        ((2, 3), 5),',
          '        ((-1, 1), 0),',
          '        ((10, -5), 5),',
          '    ]',
          '    all_passed = True',
          '    for i, (args, expected) in enumerate(test_cases):',
          '        try:',
          '            result = add(*args)',
          '            assert result == expected, f"Тест #{i+1} не пройден для входных данных {args}: получено {result}, ожидалось {expected}"',
          '            print(f"Тест #{i+1} пройден!")',
          '        except Exception as e:',
          '            print(f"Произошла ошибка: {e}", file=sys.stderr)',
          '            all_passed = False',
          '            break',
          '    if all_passed:',
          '        print("Все тесты пройдены!")', 
          'run_tests()',
        ].join('\n'),
        successMessage: 'Все тесты пройдены!',
      },
    },
    startingCode: `def add(a, b):
    # Ваш код здесь
    pass`,
  },
]
