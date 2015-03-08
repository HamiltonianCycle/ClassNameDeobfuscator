# ClassNameDeobfuscator
This is a simple script to parse through the .smali files produced by apktool and extract the .source annotation lines.

Obfuscation can be a pain to deal with when reversing an app. However, some apps do not have the `.source` annotation line removed/mangled druing the obfuscation process. This leaves the original Java class file name intact in the obfuscated code. We can abuse this to partially deobfuscate the class names.

To be clear, I am not claiming that I am the first to discover this, for lack of a better term let's call it, information leakage. However, I did stumble upon it independently while reversing an obfuscated app. Looking at a smali file, I noticed a `.source` line and a lightbulb went off. So, I threw together this script to show off the extent of what information can be revealed.  See the demo section below for some relevant Proguard details.

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
# Prepwork. Yeah, it sucks that the script needs to be in the smali dir, but I'm lazy.
apktool d com.someapp.apk
cd com.someapp/smali/
cp /path/to/ClassNameDeobfuscator.py .

# Print results to stdout:
python ClassNameDeobfuscator.py com.someapp

# Save results to file:
python ClassNameDeobfuscator.py -o /path/to/your/out.txt com.someapp
```

Using the namespace for the app as the namespace argument, in the example it's the `com.someapp` argument given to `ClassNameDeobfuscator.py`, is helpful to avoid going through thrid-party libraries and such that are included in the app. Unless, that is your goal. Use common sense and set the `namespace` according to your needs. The script will try to parse the given namespace argument into a directory structure. So, if nothing else, you can just `.`-delimit to the directory that you care about.

## Demo, Cause, & Remediation

For all the following demo, I will be using a silly little sample app I put together, [CatPurrDay](https://github.com/HamiltonianCycle/CatPurrDay/tree/master/app/src/main/java/com/catpurrday).

It would appear that new-ish versions of Android Studio (I am on Beta 0.8.6) will remove `.source` annotations with a very minimal Proguard configuration:

![Default Proguard configuration](/img/proguard-configuration.png?raw=true "Default Proguard configuration")

This was surprising, I was expecting the default configuration to illustrate the class name leaking described above.  That's great, that the default obfuscation of Proguard does remove `.source` lines.

![Script output with default Proguard configuration](/img/output-with-proguard.png?raw=true "Script output with default Proguard configuration")

Let's work backwards to see what Proguard rules could be enabled to leak class names.  The place to start this search is, of course, [the manual](https://stuff.mit.edu/afs/sipb/project/android/sdk/android-sdk-linux/tools/proguard/docs/index.html#manual/usage.html).

Sure enough, buried down in the usage is a rule called `-keepattributes`, whose description contains the following statements,

> For example, you should at least keep the Exceptions, InnerClasses, and Signature attributes when processing a library. You should also keep the SourceFile and LineNumberTable attributes for producing useful obfuscated stack traces.

Seems logical enough. Let's oblige. Rebuilding the demo app with the Proguard rule `-keepattributes SourceFile LineNumberTable` yields the following:

![Script output with -keepattributes Proguard rule enabled](/img/output-with-source-attribute.png?raw=true "Script output with -keepattributes Proguard rule enabled")

## Conclusion

In summary, even if you're obfuscating your app, you may be inadvertently leaking the class names by leaving the original source file attribute (and possibly other information!) in your obfsucated app. As we can see from the above examples, leaving the source file attribute can help a reverse engineer tremendously because it gives them whatever contextual information is present in your class names.

However, whether you want to strip these attributes out is a risk/reward trade-off you  need to consider for yourself. After all, the Proguard team isn't likely suggesting *keeping* these attributes without good reason. On the otherhand, how valuable is it to keep a reverse engineer in the dark on what your class names are? Like always, consider your situation, apply common sense, and do what's right for you.
