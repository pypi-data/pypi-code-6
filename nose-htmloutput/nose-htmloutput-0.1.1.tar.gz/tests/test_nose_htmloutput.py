from __future__ import print_function

import subprocess


def test_sample():
    subprocess.call(['nosetests', '--with-html', '--html-file=sample.html', 'tests/test_sample.py'])
    output = open('sample.html').read()

    assert """<tr>
                    <td>test_sample.MainTestCase</td>
                    <td>1</td>
                    <td>0</td>
                    <td>1</td>
                    <td>2</td>
                </tr>""" in output
    assert """<tr>
                    <td>test_sample</td>
                    <td>1</td>
                    <td>0</td>
                    <td>1</td>
                    <td>2</td>
                </tr>""" in output
    assert """<tr>
                <td><strong>Total</strong></td>
                <td>2</td>
                <td>0</td>
                <td>2</td>
                <td>4</td>
            </tr>""" in output
    assert "<h2>test_sample.MainTestCase (1 failures)</h2>" in output
    assert '<section id="test_sample.MainTestCase:test_b">' in output
    assert '<h3>test_b: <strong>' in output
    assert '<h2>test_sample (1 failures)</h2>' in output
    assert '<section id="test_sample:test_b">' in output
    assert '<h3>test_b: <strong>' in output
    assert '<h2>test_sample.MainTestCase (1 failures)</h2>' in output
    assert '<li><a class="success">test_a</a></li>' in output
    assert '<li><a class="failed" href="#test_sample.MainTestCase:test_b">test_b</a></li>' in output
    assert '<h2>test_sample (1 failures)</h2>' in output
    assert '<li><a class="success">test_a</a></li>' in output
    assert '<li><a class="failed" href="#test_sample:test_b">test_b</a></li>' in output

