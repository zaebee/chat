export interface ChallengeContent {
  title: string
  description: string
  testCases: Array<[any, any]>
  successMessage: string
}

export interface Challenge {
  id: string
  content: {
    [key: string]: ChallengeContent
  }
  startingCode: string
  functionName: string // Add functionName to Challenge interface
  visualOutput?: boolean // Add visualOutput flag
}

export const challenges: Challenge[] = [
  {
    id: '1',
    content: {
      en: {
        title: 'Add Two Numbers',
        description:
          'Write a Python function called `add` that takes two numbers as arguments and returns their sum.',
        testCases: [
          [[2, 3], 5],
          [[-1, 1], 0],
          [[10, -5], 5],
        ],
        successMessage: 'All tests passed!',
      },
      ru: {
        title: 'Сложить два числа',
        description:
          'Напишите функцию на Python с именем `add`, которая принимает два числа в качестве аргументов и возвращает их сумму.',
        testCases: [
          [[2, 3], 5],
          [[-1, 1], 0],
          [[10, -5], 5],
        ],
        successMessage: 'All tests passed!',
      },
    },
    startingCode: `def add(a, b):
    # Ваш код здесь
    pass`,
    functionName: 'add',
  },
  {
    id: '2',
    content: {
      en: {
        title: 'Multiply Two Numbers',
        description:
          'Write a Python function called `multiply` that takes two numbers as arguments and returns their product.',
        testCases: [
          [[2, 3], 6],
          [[-1, 5], -5],
          [[10, 0], 0],
        ],
        successMessage: 'All tests passed!',
      },
      ru: {
        title: 'Умножить два числа',
        description:
          'Напишите функцию на Python с именем `multiply`, которая принимает два числа в качестве аргументов и возвращает их произведение.',
        testCases: [
          [[2, 3], 6],
          [[-1, 5], -5],
          [[10, 0], 0],
        ],
        successMessage: 'All tests passed!',
      },
    },
    startingCode: `def multiply(a, b):
    # Ваш код здесь
    pass`,
    functionName: 'multiply',
  },
  {
    id: '3',
    content: {
      en: {
        title: 'Check if Even',
        description:
          'Write a Python function called `is_even` that takes an integer as an argument and returns `True` if it\'s even, `False` otherwise.',
        testCases: [
          [2, true],
          [3, false],
          [0, true],
          [-4, true],
          [-5, false],
        ],
        successMessage: 'All tests passed!',
      },
      ru: {
        title: 'Проверить на четность',
        description:
          'Напишите функцию на Python с именем `is_even`, которая принимает целое число в качестве аргумента и возвращает `True`, если оно четное, и `False` в противном случае.',
        testCases: [
          [2, true],
          [3, false],
          [0, true],
          [-4, true],
          [-5, false],
        ],
        successMessage: 'All tests passed!',
      },
    },
    startingCode: `def is_even(number):\n    # Ваш код здесь\n    pass`,
    functionName: 'is_even',
  },
  {
    id: '4',
    content: {
      en: {
        title: 'Draw a Square',
        description:
          'Use the `turtle` module to draw a square with sides of length 100. The turtle should start at (0,0) and face right.',
        testCases: [
          ['visual_test', 'no_error'],
        ],
        successMessage: 'Visual output generated!',
      },
      ru: {
        title: 'Нарисовать квадрат',
        description:
          'Используйте модуль `turtle`, чтобы нарисовать квадрат со сторонами длиной 100. Черепаха должна начинать с (0,0) и смотреть вправо.',
        testCases: [
          ['visual_test', 'no_error'],
        ],
        successMessage: 'Визуальный вывод сгенерирован!',
      },
    },
    startingCode: `import turtle\n\nturtle.resetscreen() # Reset turtle state and clear screen\nturtle.speed(1)\nturtle.forward(100)\nturtle.left(90)\nturtle.forward(100)\nturtle.left(90)\nturtle.forward(100)\nturtle.left(90)\nturtle.forward(100)\nturtle.done() # Important for Pyodide to capture output\nprint(\"Visual output generated!\") # Print success message`,    functionName: 'draw_square',    visualOutput: true,  },]
