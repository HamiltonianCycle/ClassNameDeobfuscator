# ClassNameDeobfuscator
This is a simple script to parse through the .smali files produced by apktool and extract the .source annotation lines.

Obfuscation can be a pain to deal with when reversing an app. However, some apps do not have the `.source` annotation line removed/mangled druing the obfuscation process. This leaves the original Java class file's name intact in the obfuscated code. We can abuse this to partially deobfuscate the class names.  

## Requirements
 * This assumes you have run `apktool` (or some other smali producing tool) to create smali files for the target app
 * Python 3

## Usage
Full disclosure: Only tested this on Windows using Python 3.4.2

```
usage: ClassNameDeobfuscator.py [-h] [-o output.txt] namespace

Execute in the smali directory of a disassembled APK

positional arguments:
  namespace      base namespace to begin deobfuscating classes

optional arguments:
  -h, --help     show this help message and exit
  -o output.txt  output filename to save deobfusacted class mapping
```

## Example
````
# Prepwork. Yeah, it sucks that these scripts need to be in the smali dir, but I'm lazy.
apktool d com.someapp.apk
cd com.someapp/smali/
cp /path/to/ClassNameDeobfuscator.py .
cp /path/to/SmaliFile.py .

# Print results to stdout:
python ClassNameDeobfuscator.py com.someapp

# Save results to file:
python ClassNameDeobfuscator.py -o /path/to/your/out.txt com.someapp
```

Using the namespace for the app as the namespace argument, in the example it's the `com.someapp` argument given to `ClassNameDeobfuscator.py`, is helpful to avoid going through thrid-party libraries and such that are included in the app. Unless, that is your goal. Use commonsense and set the `namespace` according to your needs.

## Coming Soon
  * Demo example
  * Remediation steps for Proguard
