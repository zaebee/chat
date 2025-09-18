export interface ChallengeContent {
  title: string
  description: string
  testCases: Array<[any, any]>
  successMessage: string
}

export enum SkillDomain {
  ITERATION = 'iteration',        // for/while loops
  FUNCTION = 'function',          // function definition/calls
  LOGIC = 'logic',                // conditionals, boolean logic
  DATA_STRUCTURE = 'data_structure',  // lists, dicts, etc.
  ALGORITHM = 'algorithm',        // sorting, searching, patterns
  DEBUG = 'debug',                // error handling, debugging
  VISUAL = 'visual',              // turtle graphics, visualization
  MATHEMATICS = 'mathematics',    // math operations, calculations
  STRING = 'string',              // string manipulation
  IO = 'io'                       // input/output operations
}

export enum ATCGPhase {
  AGGREGATE = 'A',      // Collecting/combining information
  TRANSFORMATION = 'T', // Processing/converting data
  CONNECTOR = 'C',      // Linking/communication patterns
  GENESIS = 'G'         // Creating/generating new patterns
}

export interface SkillUnlock {
  name: string
  description: string
  domain: SkillDomain
  atcgPhase: ATCGPhase
  prerequisites: string[] // skill names that must be unlocked first
  dancePattern: DancePattern
}

export interface DancePattern {
  type: 'figure8' | 'spiral' | 'zigzag' | 'circle' | 'compound'
  intensity: number        // 1-5 skill complexity
  duration: number         // dance duration in beats
  direction: number        // degrees, represents knowledge domain
  vibrationPattern: number[] // wing vibration sequence
}

export interface Challenge {
  id: string
  content: {
    [key: string]: ChallengeContent
  }
  startingCode: string
  functionName: string
  visualOutput?: boolean
  skillDomains: SkillDomain[]     // What domains this challenge covers
  skillUnlocks: SkillUnlock[]     // What skills this challenge unlocks
  atcgSequence: ATCGPhase[]       // ATCG transformation chain
  difficultyTier: number          // 1-5, affects dance complexity
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
    skillDomains: [SkillDomain.FUNCTION, SkillDomain.MATHEMATICS],
    skillUnlocks: [
      {
        name: 'Basic Arithmetic',
        description: 'Master of fundamental mathematical operations',
        domain: SkillDomain.MATHEMATICS,
        atcgPhase: ATCGPhase.AGGREGATE,
        prerequisites: [],
        dancePattern: {
          type: 'circle',
          intensity: 1,
          duration: 4,
          direction: 0, // North - representing foundational knowledge
          vibrationPattern: [1, 1, 2, 1] // Simple rhythm for basic skill
        }
      },
      {
        name: 'Function Foundation',
        description: 'Understanding of function structure and parameters',
        domain: SkillDomain.FUNCTION,
        atcgPhase: ATCGPhase.TRANSFORMATION,
        prerequisites: [],
        dancePattern: {
          type: 'figure8',
          intensity: 1,
          duration: 6,
          direction: 45, // NE - representing structured thinking
          vibrationPattern: [2, 1, 2, 1, 1, 1]
        }
      }
    ],
    atcgSequence: [ATCGPhase.AGGREGATE, ATCGPhase.TRANSFORMATION],
    difficultyTier: 1,
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
    skillDomains: [SkillDomain.FUNCTION, SkillDomain.MATHEMATICS],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.AGGREGATE, ATCGPhase.TRANSFORMATION],
    difficultyTier: 1,
  },
  {
    id: '3',
    content: {
      en: {
        title: 'Check if Even',
        description:
          "Write a Python function called `is_even` that takes an integer as an argument and returns `True` if it's even, `False` otherwise.",
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
    skillDomains: [SkillDomain.FUNCTION, SkillDomain.LOGIC],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.AGGREGATE, ATCGPhase.TRANSFORMATION],
    difficultyTier: 1,
  },
  {
    id: '4',
    content: {
      en: {
        title: 'Draw a Square',
        description:
          'Use the `turtle` module to draw a square with sides of length 100. The turtle should start at (0,0) and face right.',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Visual output generated!',
      },
      ru: {
        title: 'Нарисовать квадрат',
        description:
          'Используйте модуль `turtle`, чтобы нарисовать квадрат со сторонами длиной 100. Черепаха должна начинать с (0,0) и смотреть вправо.',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Визуальный вывод сгенерирован!',
      },
    },
    startingCode: `import turtle\n\nturtle.resetscreen() # Reset turtle state and clear screen\nturtle.speed(1)\nturtle.forward(100)\nturtle.left(90)\nturtle.forward(100)\nturtle.left(90)\nturtle.forward(100)\nturtle.left(90)\nturtle.forward(100)\nturtle.done() # Important for Pyodide to capture output\nprint(\"Visual output generated!\") # Print success message`,
    functionName: 'draw_square',
    visualOutput: true,
    skillDomains: [SkillDomain.VISUAL, SkillDomain.ITERATION],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.GENESIS],
    difficultyTier: 2,
  },
  {
    id: '5',
    content: {
      en: {
        title: 'List Explorer - Buzza\'s First Collection',
        description:
          'Buzza is learning to work with collections! Write a function called `find_max` that takes a list of numbers and returns the largest one. Help Buzza discover the power of iterating through data!',
        testCases: [
          [[1, 5, 3, 9, 2], 9],
          [[-1, -5, -3], -1],
          [[42], 42],
          [[7, 7, 7], 7],
        ],
        successMessage: 'Excellent! Buzza now understands how to explore collections systematically! 🔍',
      },
      ru: {
        title: 'Исследователь списков - Первая коллекция Buzza',
        description:
          'Buzza учится работать с коллекциями! Напишите функцию `find_max`, которая принимает список чисел и возвращает самое большое. Помогите Buzza открыть силу итерации по данным!',
        testCases: [
          [[1, 5, 3, 9, 2], 9],
          [[-1, -5, -3], -1],
          [[42], 42],
          [[7, 7, 7], 7],
        ],
        successMessage: 'Отлично! Buzza теперь понимает, как систематически исследовать коллекции! 🔍',
      },
    },
    startingCode: `def find_max(numbers):
    # Buzza's curiosity leads her to explore each number
    # Help her find the largest one!
    pass`,
    functionName: 'find_max',
    skillDomains: [SkillDomain.DATA_STRUCTURE, SkillDomain.ITERATION, SkillDomain.ALGORITHM],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.AGGREGATE, ATCGPhase.TRANSFORMATION],
    difficultyTier: 2,
  },
  {
    id: '6',
    content: {
      en: {
        title: 'String Patterns - Buzza\'s Word Weaving',
        description:
          'Buzza is learning about patterns! Write a function called `count_vowels` that counts how many vowels (a, e, i, o, u) are in a word. This will help Buzza understand pattern recognition!',
        testCases: [
          ['hello', 2],
          ['python', 1],
          ['education', 5],
          ['xyz', 0],
          ['AEIOU', 5],
        ],
        successMessage: 'Amazing pattern recognition! Buzza\'s analytical skills are growing! 🧩',
      },
      ru: {
        title: 'Строковые шаблоны - Плетение слов Buzza',
        description:
          'Buzza изучает шаблоны! Напишите функцию `count_vowels`, которая подсчитывает гласные (a, e, i, o, u) в слове. Это поможет Buzza понять распознавание шаблонов!',
        testCases: [
          ['hello', 2],
          ['python', 1],
          ['education', 5],
          ['xyz', 0],
          ['AEIOU', 5],
        ],
        successMessage: 'Удивительное распознавание шаблонов! Аналитические навыки Buzza растут! 🧩',
      },
    },
    startingCode: `def count_vowels(word):
    # Buzza needs to examine each letter
    # Count the vowels: a, e, i, o, u (both lowercase and uppercase)
    pass`,
    functionName: 'count_vowels',
    skillDomains: [SkillDomain.STRING, SkillDomain.ITERATION],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.AGGREGATE, ATCGPhase.TRANSFORMATION],
    difficultyTier: 2,
  },
  {
    id: '7',
    content: {
      en: {
        title: 'Logic Gates - Buzza\'s Decision Making',
        description:
          'Buzza is developing decision-making skills! Write a function called `categorize_number` that takes a number and returns "positive", "negative", or "zero". This builds Buzza\'s logical thinking!',
        testCases: [
          [5, 'positive'],
          [-3, 'negative'],
          [0, 'zero'],
          [100, 'positive'],
          [-1, 'negative'],
        ],
        successMessage: 'Perfect logical thinking! Buzza\'s decision-making framework is solid! ⚡',
      },
      ru: {
        title: 'Логические врата - Принятие решений Buzza',
        description:
          'Buzza развивает навыки принятия решений! Напишите функцию `categorize_number`, которая принимает число и возвращает "positive", "negative" или "zero". Это развивает логическое мышление Buzza!',
        testCases: [
          [5, 'positive'],
          [-3, 'negative'],
          [0, 'zero'],
          [100, 'positive'],
          [-1, 'negative'],
        ],
        successMessage: 'Идеальное логическое мышление! Система принятия решений Buzza солидна! ⚡',
      },
    },
    startingCode: `def categorize_number(num):
    # Buzza needs to make logical decisions
    # Return "positive", "negative", or "zero"
    pass`,
    functionName: 'categorize_number',
    skillDomains: [SkillDomain.LOGIC, SkillDomain.FUNCTION],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.AGGREGATE, ATCGPhase.TRANSFORMATION],
    difficultyTier: 2,
  },
  {
    id: '8',
    content: {
      en: {
        title: 'Loop Mastery - Buzza\'s Repetition Power',
        description:
          'Buzza is learning the power of repetition! Write a function called `sum_range` that calculates the sum of all numbers from 1 to n (inclusive). This teaches Buzza about efficient iteration!',
        testCases: [
          [5, 15], // 1+2+3+4+5 = 15
          [1, 1],
          [10, 55], // 1+2+...+10 = 55
          [3, 6], // 1+2+3 = 6
        ],
        successMessage: 'Fantastic! Buzza has mastered the art of repetition and accumulation! 🔄',
      },
      ru: {
        title: 'Мастерство циклов - Сила повторения Buzza',
        description:
          'Buzza изучает силу повторения! Напишите функцию `sum_range`, которая вычисляет сумму всех чисел от 1 до n (включительно). Это учит Buzza эффективной итерации!',
        testCases: [
          [5, 15], // 1+2+3+4+5 = 15
          [1, 1],
          [10, 55], // 1+2+...+10 = 55
          [3, 6], // 1+2+3 = 6
        ],
        successMessage: 'Фантастика! Buzza освоила искусство повторения и накопления! 🔄',
      },
    },
    startingCode: `def sum_range(n):
    # Buzza needs to add up all numbers from 1 to n
    # Use the power of loops!
    pass`,
    functionName: 'sum_range',
    skillDomains: [SkillDomain.ITERATION, SkillDomain.ALGORITHM],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.AGGREGATE, ATCGPhase.TRANSFORMATION],
    difficultyTier: 3,
  },
  {
    id: '9',
    content: {
      en: {
        title: 'Data Structures - Buzza\'s Organization Skills',
        description:
          'Buzza is learning to organize data efficiently! Write a function called `word_lengths` that takes a list of words and returns a list of their lengths. This develops Buzza\'s data transformation abilities!',
        testCases: [
          [['hello', 'world'], [5, 5]],
          [['python', 'code'], [6, 4]],
          [['a', 'bee', 'coding'], [1, 3, 6]],
          [[], []],
        ],
        successMessage: 'Brilliant data organization! Buzza\'s transformation skills are evolving! 🗂️',
      },
      ru: {
        title: 'Структуры данных - Навыки организации Buzza',
        description:
          'Buzza учится эффективно организовывать данные! Напишите функцию `word_lengths`, которая принимает список слов и возвращает список их длин. Это развивает способности Buzza к преобразованию данных!',
        testCases: [
          [['hello', 'world'], [5, 5]],
          [['python', 'code'], [6, 4]],
          [['a', 'bee', 'coding'], [1, 3, 6]],
          [[], []],
        ],
        successMessage: 'Блестящая организация данных! Навыки трансформации Buzza развиваются! 🗂️',
      },
    },
    startingCode: `def word_lengths(words):
    # Buzza needs to transform a list of words into their lengths
    # Return a new list with the length of each word
    pass`,
    functionName: 'word_lengths',
    skillDomains: [SkillDomain.DATA_STRUCTURE, SkillDomain.ITERATION],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.AGGREGATE, ATCGPhase.TRANSFORMATION],
    difficultyTier: 3,
  },
  {
    id: '10',
    content: {
      en: {
        title: 'Advanced Logic - Buzza\'s Metamorphosis Challenge',
        description:
          'Buzza is ready for her metamorphosis challenge! Write a function called `is_prime` that checks if a number is prime (only divisible by 1 and itself). This complex logic will trigger Buzza\'s evolution to Larva stage!',
        testCases: [
          [2, true],
          [3, true],
          [4, false],
          [17, true],
          [25, false],
          [1, false],
        ],
        successMessage: 'METAMORPHOSIS ACHIEVED! 🐛➡️🦋 Buzza has evolved to Larva stage through advanced logical reasoning!',
      },
      ru: {
        title: 'Продвинутая логика - Вызов метаморфозы Buzza',
        description:
          'Buzza готова к вызову метаморфозы! Напишите функцию `is_prime`, которая проверяет, является ли число простым (делится только на 1 и само себя). Эта сложная логика запустит эволюцию Buzza в стадию личинки!',
        testCases: [
          [2, true],
          [3, true],
          [4, false],
          [17, true],
          [25, false],
          [1, false],
        ],
        successMessage: 'МЕТАМОРФОЗА ДОСТИГНУТА! 🐛➡️🦋 Buzza эволюционировала в стадию личинки через продвинутое логическое мышление!',
      },
    },
    startingCode: `def is_prime(num):
    # Buzza's ultimate challenge before metamorphosis!
    # A number is prime if it's only divisible by 1 and itself
    # Special cases: numbers less than 2 are not prime
    pass`,
    functionName: 'is_prime',
    skillDomains: [SkillDomain.LOGIC, SkillDomain.ALGORITHM],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.AGGREGATE, ATCGPhase.TRANSFORMATION],
    difficultyTier: 4,
  },
  {
    id: '11',
    content: {
      en: {
        title: 'For Loop Basics - Counting Stars',
        description:
          'Learn the `for` loop by drawing stars! Use a for loop to print 5 stars (*) in a row. This teaches basic iteration and repetition concepts.',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Perfect! You\'ve mastered basic for loops! ⭐',
      },
      ru: {
        title: 'Основы цикла for - Считаем звёзды',
        description:
          'Изучите цикл `for`, рисуя звёзды! Используйте цикл for, чтобы напечатать 5 звёзд (*) в ряд. Это учит базовым концепциям итерации и повторения.',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Отлично! Вы освоили основы циклов for! ⭐',
      },
    },
    startingCode: `# Рисуем 5 звёзд с помощью цикла for
for i in range(5):
    print("*", end="")  # end="" означает печать в одной строке
print()  # Переход на новую строку в конце
print("Готово!")`,
    functionName: 'draw_stars',
    skillDomains: [SkillDomain.ITERATION],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.GENESIS],
    difficultyTier: 1,
  },
  {
    id: '12',
    content: {
      en: {
        title: 'While Loop Adventure - Number Guessing',
        description:
          'Create a simple number guessing game using a while loop! The computer thinks of number 7, and you keep guessing until you get it right.',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Excellent! You understand while loops! 🎯',
      },
      ru: {
        title: 'Приключение с циклом while - Угадай число',
        description:
          'Создайте простую игру угадывания числа с циклом while! Компьютер загадывает число 7, и вы угадываете, пока не угадаете правильно.',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Отлично! Вы понимаете циклы while! 🎯',
      },
    },
    startingCode: `# Игра "Угадай число" с циклом while
secret_number = 7
guess = 0

print("Угадайте число от 1 до 10!")

while guess != secret_number:
    guess = int(input("Введите ваше число: "))
    if guess < secret_number:
        print("Слишком маленько! Попробуйте больше.")
    elif guess > secret_number:
        print("Слишком большо! Попробуйте меньше.")
    else:
        print("🎉 Поздравляю! Вы угадали число", secret_number)

print("Игра окончена!")`,
    functionName: 'number_guessing_game',
    skillDomains: [SkillDomain.ITERATION, SkillDomain.LOGIC, SkillDomain.IO],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.CONNECTOR, ATCGPhase.TRANSFORMATION],
    difficultyTier: 2,
  },
  {
    id: '13',
    content: {
      en: {
        title: 'Turtle Squares - For Loop with Graphics',
        description:
          'Use turtle graphics with a for loop to draw a colorful square! Learn how loops make drawing shapes easier and more fun.',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Amazing! You combined loops with turtle graphics! 🐢🎨',
      },
      ru: {
        title: 'Черепашьи квадраты - Цикл for с графикой',
        description:
          'Используйте графику черепашки с циклом for, чтобы нарисовать цветной квадрат! Узнайте, как циклы делают рисование фигур проще и веселее.',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Потрясающе! Вы объединили циклы с графикой черепашки! 🐢🎨',
      },
    },
    startingCode: `import turtle

# Настройка черепашки
turtle.resetscreen()
turtle.speed(3)
turtle.color("blue")

# Рисуем квадрат с помощью цикла for
for i in range(4):  # 4 стороны квадрата
    turtle.forward(100)  # Двигаемся вперёд на 100 пикселей
    turtle.right(90)     # Поворачиваем направо на 90 градусов
    print(f"Нарисована сторона {i + 1}")

# Финиш
turtle.done()
print("Квадрат готов! 🟦")`,
    functionName: 'turtle_square',
    visualOutput: true,
    skillDomains: [SkillDomain.VISUAL, SkillDomain.ITERATION],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.GENESIS],
    difficultyTier: 2,
  },
  {
    id: '14',
    content: {
      en: {
        title: 'Turtle Spiral - While Loop Magic',
        description:
          'Create a beautiful spiral using turtle and a while loop! Watch as the turtle draws an expanding spiral with changing colors.',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Incredible! You created art with while loops! 🌀✨',
      },
      ru: {
        title: 'Черепашья спираль - Магия цикла while',
        description:
          'Создайте красивую спираль, используя черепашку и цикл while! Смотрите, как черепашка рисует расширяющуюся спираль с изменяющимися цветами.',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Невероятно! Вы создали искусство с циклами while! 🌀✨',
      },
    },
    startingCode: `import turtle

# Настройка
turtle.resetscreen()
turtle.speed(6)
turtle.bgcolor("black")

# Переменные для спирали
distance = 10
angle = 90
colors = ["red", "orange", "yellow", "green", "blue", "purple"]

# Рисуем спираль с циклом while
step = 0
while distance < 100:  # Пока расстояние меньше 100
    # Меняем цвет
    turtle.color(colors[step % len(colors)])

    # Рисуем линию и поворачиваем
    turtle.forward(distance)
    turtle.right(angle)

    # Увеличиваем расстояние для следующего шага
    distance += 2
    step += 1

    print(f"Шаг {step}: расстояние = {distance}")

turtle.done()
print("Спираль готова! 🌀")`,
    functionName: 'turtle_spiral',
    visualOutput: true,
    skillDomains: [SkillDomain.VISUAL, SkillDomain.ITERATION, SkillDomain.LOGIC],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.GENESIS, ATCGPhase.TRANSFORMATION],
    difficultyTier: 3,
  },
  {
    id: '15',
    content: {
      en: {
        title: 'Nested Loops - Turtle Flower Garden',
        description:
          'Advanced challenge! Use nested for loops (loop inside a loop) to draw a flower garden with turtle graphics. Perfect for students ready for more complex patterns!',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Master level achieved! You understand nested loops! 🌸🌻🌺',
      },
      ru: {
        title: 'Вложенные циклы - Черепашій сад цветов',
        description:
          'Продвинутый вызов! Используйте вложенные циклы for (цикл внутри цикла), чтобы нарисовать сад цветов с графикой черепашки. Идеально для студентов, готовых к более сложным узорам!',
        testCases: [['visual_test', 'no_error']],
        successMessage: 'Достигнут мастерский уровень! Вы понимаете вложенные циклы! 🌸🌻🌺',
      },
    },
    startingCode: `import turtle

# Настройка
turtle.resetscreen()
turtle.speed(8)
turtle.bgcolor("lightgreen")

def draw_flower(size, color):
    """Рисует один цветок"""
    turtle.color(color)
    # Рисуем лепестки (внутренний цикл)
    for petal in range(6):  # 6 лепестков
        turtle.circle(size)
        turtle.right(60)

def draw_garden():
    """Рисует сад из цветов (внешний цикл)"""
    flowers = 3
    colors = ["red", "pink", "yellow"]

    # Внешний цикл - количество цветов
    for flower_num in range(flowers):
        # Выбираем позицию для цветка
        turtle.penup()
        turtle.goto(-100 + flower_num * 100, 0)
        turtle.pendown()

        # Рисуем цветок (вызывает внутренний цикл)
        draw_flower(20, colors[flower_num])

        print(f"Цветок {flower_num + 1} готов!")

# Рисуем сад
draw_garden()

turtle.hideturtle()
turtle.done()
print("Сад цветов готов! 🌻")`,
    functionName: 'turtle_flower_garden',
    visualOutput: true,
    skillDomains: [SkillDomain.VISUAL, SkillDomain.ITERATION, SkillDomain.FUNCTION],
    skillUnlocks: [],
    atcgSequence: [ATCGPhase.GENESIS, ATCGPhase.TRANSFORMATION],
    difficultyTier: 4,
  },
]

// Add types for organella skill system
type OrganellaType = 'mathematical' | 'logical' | 'creative' | 'memory' | 'sensory' | 'motor'

// Personal Skill Mutation Ecosystem
interface PersonalSkillRegistry {
  playerId: string
  organellas: Map<OrganellaType, OrganellaSkillset>
  activeMutations: ATCGMutation[]
  danceHistory: DanceEvent[]
  crossPollinationEvents: CrossPollinationEvent[]
}

interface OrganellaSkillset {
  type: OrganellaType
  baseSkills: SkillUnlock[]         // From individual challenge completions
  mutatedSkills: CompoundSkill[]    // From ATCG chains
  evolutionLevel: number            // How advanced this organella has become
  specializations: string[]         // Unique abilities this organella has developed
}

interface CompoundSkill {
  name: string
  description: string
  sourceSkills: string[]            // Which base skills combined
  atcgChain: ATCGPhase[]           // The mutation sequence that created it
  manifestation: DancePattern       // How this skill expresses through dance
  crossPollinationPotential: OrganellaType[] // Which other organellas can benefit
}

interface ATCGMutation {
  id: string
  fromSkill: string
  toSkill: string
  phase: ATCGPhase
  triggeredBy: 'completion' | 'time' | 'synergy' | 'dance_resonance'
  timestamp: Date
  energyCost: number
}

interface DanceEvent {
  id: string
  skillName: string
  organellaType: OrganellaType
  pattern: DancePattern
  witnesses: OrganellaType[]        // Other organellas that observed
  resonanceEffects: ResonanceEffect[]
  timestamp: Date
}

interface ResonanceEffect {
  targetOrganella: OrganellaType
  effectType: 'skill_boost' | 'new_mutation' | 'cross_pollination'
  intensity: number
  duration: number
}

interface CrossPollinationEvent {
  id: string
  sourceOrganella: OrganellaType
  targetOrganella: OrganellaType
  sourceSkill: string
  resultingSkill: string
  danceSequence: DancePattern[]
  timestamp: Date
}

// **YOUR PERSONAL SKILL ECOSYSTEM** - How completed challenges become living abilities
const examplePlayerSkillRegistry: PersonalSkillRegistry = {
  playerId: 'zaebee_hive_commander',
  organellas: new Map([
    ['mathematical', {
      type: 'mathematical',
      baseSkills: [
        // FROM YOUR CHALLENGE #1 COMPLETION → SKILL DNA EXTRACTED
        {
          name: 'Basic Arithmetic',
          description: 'Master of fundamental mathematical operations',
          domain: SkillDomain.MATHEMATICS,
          atcgPhase: ATCGPhase.AGGREGATE,
          prerequisites: [],
          dancePattern: {
            type: 'circle',
            intensity: 1,
            duration: 4,
            direction: 0, // Foundation knowledge facing North
            vibrationPattern: [1, 1, 2, 1] // Your arithmetic signature
          }
        }
      ],
      mutatedSkills: [
        // ATCG MUTATION: Basic Arithmetic + Function Foundation → NEW COMPOUND SKILL
        {
          name: 'Mathematical Function Mastery',
          description: 'Fusion of arithmetic precision with functional thinking - your unique synthesis',
          sourceSkills: ['Basic Arithmetic', 'Function Foundation'],
          atcgChain: [ATCGPhase.AGGREGATE, ATCGPhase.TRANSFORMATION],
          manifestation: {
            type: 'compound',
            intensity: 2,
            duration: 8,
            direction: 90, // Advanced knowledge facing East
            vibrationPattern: [2, 1, 2, 1, 1, 1, 1, 2] // Merged dance patterns from both skills
          },
          crossPollinationPotential: ['logical', 'creative'] // Can teach other organellas
        }
      ],
      evolutionLevel: 2, // Evolved through skill mutation
      specializations: ['numerical_intuition', 'pattern_recognition'] // Emergent abilities
    }],
    ['logical', {
      type: 'logical',
      baseSkills: [
        // FROM YOUR CHALLENGE #1 COMPLETION → SKILL DNA EXTRACTED
        {
          name: 'Function Foundation',
          description: 'Understanding of function structure and parameters',
          domain: SkillDomain.FUNCTION,
          atcgPhase: ATCGPhase.TRANSFORMATION,
          prerequisites: [],
          dancePattern: {
            type: 'figure8',
            intensity: 1,
            duration: 6,
            direction: 45, // Structured thinking NE
            vibrationPattern: [2, 1, 2, 1, 1, 1] // Your function signature
          }
        }
      ],
      mutatedSkills: [], // Will evolve as you complete more challenges
      evolutionLevel: 1,
      specializations: ['structural_thinking']
    }]
  ]),
  activeMutations: [
    // LIVE MUTATION EVENT: Your skills transforming in real-time
    {
      id: 'mut_zaebee_001',
      fromSkill: 'Basic Arithmetic',
      toSkill: 'Mathematical Function Mastery',
      phase: ATCGPhase.TRANSFORMATION,
      triggeredBy: 'synergy', // Skills found each other and combined
      timestamp: new Date(),
      energyCost: 15 // Mental energy required for skill fusion
    }
  ],
  danceHistory: [
    // YOUR BEE DANCES: When you activated Function Foundation skill
    {
      id: 'dance_zaebee_001',
      skillName: 'Function Foundation',
      organellaType: 'logical',
      pattern: {
        type: 'figure8',
        intensity: 1,
        duration: 6,
        direction: 45,
        vibrationPattern: [2, 1, 2, 1, 1, 1]
      },
      witnesses: ['mathematical'], // Mathematical organella observed this dance
      resonanceEffects: [
        {
          targetOrganella: 'mathematical',
          effectType: 'cross_pollination',
          intensity: 0.8,
          duration: 24 // Effect lasts 24 hours
        }
      ],
      timestamp: new Date()
    }
  ],
  crossPollinationEvents: [
    // CROSS-POLLINATION: Skills sharing between your organellas
    {
      id: 'cross_zaebee_001',
      sourceOrganella: 'logical',
      targetOrganella: 'mathematical',
      sourceSkill: 'Function Foundation',
      resultingSkill: 'Mathematical Function Mastery',
      danceSequence: [
        // First: Logical organella performs Function Foundation dance
        {
          type: 'figure8',
          intensity: 1,
          duration: 6,
          direction: 45,
          vibrationPattern: [2, 1, 2, 1, 1, 1]
        },
        // Then: Mathematical organella responds with Arithmetic dance
        {
          type: 'circle',
          intensity: 1,
          duration: 4,
          direction: 0,
          vibrationPattern: [1, 1, 2, 1]
        }
      ],
      timestamp: new Date()
    }
  ]
}

export { Challenge, examplePlayerSkillRegistry }

export type {
  SkillDomain,
  ATCGPhase,
  SkillUnlock,
  DancePattern,
  PersonalSkillRegistry,
  OrganellaSkillset,
  CompoundSkill,
  ATCGMutation,
  DanceEvent,
  ResonanceEffect,
  CrossPollinationEvent,
  OrganellaType
}
