import unittest
from pathlib import Path

from llm_web_kit.libs.html_utils import html_to_element
from llm_web_kit.pipeline.extractor.html.recognizer.cc_math.common import \
    CCMATH
from llm_web_kit.pipeline.extractor.html.recognizer.ccmath import \
    MathRecognizer
from llm_web_kit.pipeline.extractor.html.recognizer.recognizer import CCTag

TEST_CASES = [
    # 基本公式测试用例
    {
        'input': [
            (
                ('<p>这是p的text<span class="mathjax_display">'
                 '$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>'
                 '这是b的tail</p>'),
                ('<p>这是p的text<span class="mathjax_display">'
                 '$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>'
                 '这是b的tail</p>')
            )
        ],
        'raw_html': (
            '<head> '
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js'
            '?config=TeX-MML-AM_CHTML"> </script> '
            '</head> '
            '<p>这是p的text<span class="mathjax_display">$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>'
        ),
        'expected': [
            (
                '<p>这是p的text</p>',
                '<p>这是p的text</p>'
            ),
            (
                '<p><ccmath-interline type="latex" by="mathjax" html=\'&lt;span class="mathjax_display"&gt;$$a^2 + b^2 = c^2$$&lt;/span&gt;这是span的tail\'>$$a^2 + b^2 = c^2$$</ccmath-interline></p>',
                '<span class="mathjax_display">$$a^2 + b^2 = c^2$$</span>这是span的tail'
            ),
            (
                '<p>这是span的tail<b>这是b的text</b>这是b的tail</p>',
                '<p>这是span的tail<b>这是b的text</b>这是b的tail</p>'
            )
        ]
    },
    #2
    {
        'input': [
            (
                ('<p>this is p text<span class="katex" id="form1">'
                '</span>this is span1 tail<span class="katex" id="form2"></span>this is span2 tail<b>this is b text</b>'
                'this is b tail'
                '<script>'
                'var fotm = document.getElementById("form1")'
                'katex.render("E = mc^2", fotm);'
                'katex.render("a^2 + b^2 = c^2", form2);'
                '</script>'
                '</p>'),
                (
                '<p>this is p text<span class="katex" id="form1">'
                '</span>this is span1 tail<span class="katex" id="form2"></span>this is span2 tail<b>this is b text</b>'
                'this is b tail'
                '<script>'
                'var fotm = document.getElementById("form1")'
                'katex.render("E = mc^2", fotm);'
                'katex.render("a^2 + b^2 = c^2", form2);'
                '</script>'
                '</p>')
            )
        ],
        'raw_html': (
            '<head> '
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css">'
            '</head> '
            '<p>this is p text<span class="katex">$E = mc^2$</span>this is span1 tail<span class="katex">$a^2 + b^2 = c^2$</span>this is span2 tail<b>this is b text</b>this is b tail<script>var fotm = document.getElementById("form1")katex.render("E = mc^2", fotm);katex.render("a^2 + b^2 = c^2", form2);</script></p>'
        ),
        'expected': [
            (
                '<p>this is p text<ccmath-inline>$E = mc^2$</ccmath-inline>this is span1 tail<ccmath-inline>$a^2 + b^2 = c^2$</ccmath-inline>this is span2 tail<b>this is b text</b>this is b tail<script>var fotm = document.getElementById("form1")katex.render("E = mc^2", fotm);katex.render("a^2 + b^2 = c^2", form2);</script></p>', 
                '<p>this is p text<ccmath-inline>$E = mc^2$</ccmath-inline>this is span1 tail<ccmath-inline>$a^2 + b^2 = c^2$</ccmath-inline>this is span2 tail<b>this is b text</b>this is b tail<script>var fotm = document.getElementById("form1")katex.render("E = mc^2", fotm);katex.render("a^2 + b^2 = c^2", form2);</script></p>'
            )
        ]
    },
    # 已经包含cccode标签
    # {
    #     'input': [
    #         ('<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>',
    #          '<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>')
    #     ],
    #     'raw_html': '<span class=mathjax>Some text with a formula $$x = 5$$ in it.</span>',
    #     'expected': [
    #         ('<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>',
    #          '<cccode class=mathjax>Some text with a formula $$x = 5$$ in it.</cccode>')
    #     ]
    # },
    # html_list包含多个html，class=MathJax_Display
    # {
    #     'input': [
    #         ('<p>This is a test.</p>', '<p>This is a test.</p>'),
    #         ('<span class=Mathjax_display>$$a^2 + b^2 = c^2$$</span>',
    #          '<span class=Mathjax_display>$$a^2 + b^2 = c^2$$</span>')
    #     ],
    #     'raw_html': '<p>This is a test.</p> <span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>',
    #     'expected': [
    #         ('<p>This is a test.</p>', '<p>This is a test.</p>'),
    #         ('<ccmath type="latex">$$a^2 + b^2 = c^2$$</ccmath>',
    #          '<span class=Mathjax_display>$$a^2 + b^2 = c^2$$</span>')
    #     ]
    # },
    # raw_html包含mathjax渲染器定义，class=mathjax_display
    # {
    #     'input': [
    #         ('<p>这是p的text<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>'),
    #         ('<p>这是p的text<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>')
    #     ],
    #     'raw_html': (
    #         '<head> '
    #         '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js'
    #         '?config=TeX-MML-AM_CHTML"> </script> '
    #         '</head> '
    #         '<p>这是p的text<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>'
    #     ),
    #     'expected': [
    #         ('<p>这是p的text<ccmath type="latex" by="mathjax">$$a^2 + b^2 = c^2$$</ccmath>这是span的tail<b>这是b的text</b>这是b的tail</p>',
    #          '<p>这是p的text<span class=mathjax_display>$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>')
    #     ]
    # }
]

TEST_CASES_HTML = [
    # math-container, latex + mathjax
    {
        'input': ['assets/ccmath/stackexchange_1_span-math-container_latex_mathjax.html'],
        'base_url': 'https://worldbuilding.stackexchange.com/questions/162264/is-there-a-safe-but-weird-distance-from-black-hole-merger',
        'expected': [
            'assets/ccmath/stackexchange_1_interline_1.html',
            'assets/ccmath/stackexchange_1_interline_2.html',
        ],
    },
    {
        'input': [
            'assets/ccmath/libretexts_1_p_latex_mathjax.html',
        ],
        'base_url': 'https://math.libretexts.org/Under_Construction/Purgatory/Remixer_University/Username%3A_pseeburger/MTH_098_Elementary_Algebra/1%3A_Foundations/1.5%3A_Multiply_and_Divide_Integers',
        'expected': [
            # 'assets/ccmath/libretexts_1_interline_1.html',
        ],
    },
    {
        'input': [
            'assets/ccmath/wikipedia_1_math_annotation.html',
        ],
        'base_url': 'https://en.m.wikipedia.org/wiki/Equicontinuity',
        'expected': [
            # 'assets/ccmath/wikipedia_1_interline_1.html',
        ],
    },
    {
        'input': [
            'assets/ccmath/mathjax-mml-chtml.html',
        ],
        'base_url': 'https://mathjax.github.io/MathJax-demos-web/tex-chtml.html',
        'expected': [
            'assets/ccmath/mathjax-mml-chtml_interline_1.html',
            'assets/ccmath/mathjax-mml-chtml_interline_2.html',
            'assets/ccmath/mathjax-mml-chtml_interline_3.html',
            'assets/ccmath/mathjax-mml-chtml_interline_4.html',
            'assets/ccmath/mathjax-mml-chtml_interline_5.html',
            'assets/ccmath/mathjax-mml-chtml_interline_6.html',
            'assets/ccmath/mathjax-mml-chtml_interline_7.html',
            'assets/ccmath/mathjax-mml-chtml_interline_8.html',
        ],
    }
]

TEST_EQUATION_TYPE = [
    {
        'input': '<span>$$a^2 + b^2 = c^2$$</span>',
        'expected': ('equation-interline', 'latex')
    },
    {
        'input': '<span>$a^2 + b^2 = c^2$</span>',
        'expected': ('equation-inline', 'latex')
    },
    {
        'input': '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>',
        'expected': ('equation-inline', 'mathml')
    },
    {
        'input': '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>',
        'expected': ('equation-interline', 'mathml')
    },
    {
        'input': '<span>x<sub>1</sub> + x<sup>2</sup></span>',
        'expected': ('equation-inline', 'htmlmath')
    },
    # {
    #     'input': '<p>Matrices: <code>[[a,b],[c,d]]</code> yields to `[[a,b],[c,d]]`</p>',
    #     'expected': ('equation-inline', 'asciimath')
    # },
    {
        'input': '<p>Matrices: <code>[[a,b],[c,d]]</code> </p>',
        'expected': (None, None)
    }
]

TEST_CONTENT_LIST_NODE = [
    {
        'input': (
            'https://www.baidu.com',
            '<html><body><p><ccmath-interline type="latex" by="mathjax" html="&lt;span class=&quot;math-container&quot;&gt;$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$&lt;/span&gt;">$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$</ccmath-interline></p></body></html>',
            '<span class="math-container">$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$</span>'
        ),
        'expected': {
            'type': 'equation-interline',
            'raw_content': '<span class="math-container">$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$</span>',
            'content': {
                'math_content': '$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$',
                'math_type': 'latex',
                'by': 'mathjax'
            }
        }
    }
]

TEST_GET_MATH_RENDER = [
    {
        'input': [
            'assets/ccmath/stackexchange_1_span-math-container_latex_mathjax.html'
        ],
        'base_url': 'https://worldbuilding.stackexchange.com/questions/162264/is-there-a-safe-but-weird-distance-from-black-hole-merger',
        'expected': 'mathjax',
    },
    {
        'input': [
            'assets/ccmath/libretexts_1_p_latex_mathjax.html',
        ],
        'base_url': 'https://math.libretexts.org/Under_Construction/Purgatory/Remixer_University/Username%3A_pseeburger/MTH_098_Elementary_Algebra/1%3A_Foundations/1.5%3A_Multiply_and_Divide_Integers',
        'expected': 'mathjax',
    }
]

base_dir = Path(__file__).parent


class TestMathRecognizer(unittest.TestCase):
    def setUp(self):
        self.math_recognizer = MathRecognizer()

    def test_math_recognizer(self):
        for test_case in TEST_CASES:
            with self.subTest(input=test_case['input'], raw_html=test_case['raw_html']):
                output_html = self.math_recognizer.recognize(
                    'https://www.baidu.com',
                    test_case['input'],
                    test_case['raw_html']
                )
                print(output_html)
                self.assertEqual(len(output_html), len(test_case['expected']), msg=f'result is: {len(output_html)}, expected is: {len(test_case["expected"])}')
                for i in range(len(output_html)):
                    self.assertEqual(output_html[i], test_case['expected'][i], msg=f'result is: {output_html[i]}, expected is: {test_case["expected"][i]}')

    def test_math_recognizer_html(self):
        for test_case in TEST_CASES_HTML:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            base_url = test_case['base_url']
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.math_recognizer.recognize(base_url, [(raw_html, raw_html)], raw_html)
            print(len(parts))
            # 将parts列表中第一个元素拼接保存到文件，带随机数
            # import random
            # with open('parts'+str(random.randint(1, 100))+".html", 'w') as f:
            #     for part in parts:
            #         f.write(str(part[0]))
            parts = [part[0] for part in parts if CCTag.CC_MATH_INTERLINE in part[0]]
            self.assertEqual(len(parts), len(test_case['expected']))
            for expect_path, part in zip(test_case['expected'], parts):
                expect = base_dir.joinpath(expect_path).read_text(encoding='utf-8').strip()
                a_tree = html_to_element(part)
                a_result = a_tree.xpath(f'.//{CCTag.CC_MATH_INTERLINE}')[0]
                answer = a_result.text
                print('part::::::::', part.encode('utf-8'))
                print('answer::::::::', answer.encode('utf-8'))
                # print('expect::::::::', expect)
                self.assertEqual(expect, answer)

    def test_to_content_list_node(self):
        for test_case in TEST_CONTENT_LIST_NODE:
            with self.subTest(input=test_case['input']):
                output_node = self.math_recognizer.to_content_list_node(
                    test_case['input'][0],
                    test_case['input'][1],
                    test_case['input'][2]
                )
                self.assertEqual(output_node, test_case['expected'])

        # 测试没有ccmath标签的情况
        invalid_content = (
            'https://www.baidu.com',
            '<div>Some math content</div>',
            '<div>Some math content</div>'
        )
        with self.assertRaises(ValueError) as exc_info:
            self.math_recognizer.to_content_list_node(
                invalid_content[0],
                invalid_content[1],
                invalid_content[2]
            )
        self.assertIn('No ccmath element found in content', str(exc_info.exception))


class TestCCMATH(unittest.TestCase):
    def setUp(self):
        self.ccmath = CCMATH()

    def test_get_equation_type(self):
        for test_case in TEST_EQUATION_TYPE:
            with self.subTest(input=test_case['input']):
                equation_type, math_type = self.ccmath.get_equation_type(test_case['input'])
                print('input::::::::', test_case['input'])
                self.assertEqual(equation_type, test_case['expected'][0], msg=f'result is: {equation_type}, expected is: {test_case["expected"][0]}')
                self.assertEqual(math_type, test_case['expected'][1], msg=f'result is: {math_type}, expected is: {test_case["expected"][1]}')

    def test_get_math_render(self):
        for test_case in TEST_GET_MATH_RENDER:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            raw_html = raw_html_path.read_text()
            output_render = self.ccmath.get_math_render(raw_html)
            self.assertEqual(output_render, test_case['expected'])


if __name__ == '__main__':
    r = TestMathRecognizer()
    r.setUp()
    r.test_math_recognizer()
    r.test_math_recognizer_html()
    # r.test_to_content_list_node()
    # html = r'<p class="lt-math-15120">\[\begin{array} {ll} {5 \cdot 3 = 15} &amp;{-5(3) = -15} \\ {5(-3) = -15} &amp;{(-5)(-3) = 15} \end{array}\]</p>'
    # tree = html_to_element(html)
    # print(tree.text)

    # raw_html_path = base_dir.joinpath('assets/ccmath/mathjax-mml-chtml.html')
    # raw_html = raw_html_path.read_text()
    # from llm_web_kit.libs.html_utils import build_html_tree
    # tree = build_html_tree(raw_html)
    # for node in tree.iter():
    #     print(node.tag)

    # c = TestCCMATH()
    # c.setUp()
    # c.test_get_equation_type()
