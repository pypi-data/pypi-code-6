plugin_xml = '''<?xml version="1.0"?>
<plugin id="Gnumeric_JkFuncPlugin">
  <information>
    <name>Sheetmusic</name>
    <description>Make music from spreadsheets</description>
  </information>
  <loader type="Gnumeric_PythonLoader:python">
    <attribute name="module_name" value="sheetmusic"/>
  </loader>
  <services>
    <service type="function_group" id="sheetmusic">
      <category>Local Python</category>
      <functions>
      </functions>
    </service>
  </services>
</plugin>
'''

sheetmusic_py = '''import libsheetmusic.main
sheetmusic_functions = libsheetmusic.main.functions()
'''
