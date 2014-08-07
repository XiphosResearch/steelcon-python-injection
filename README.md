SteelCon 2014 - Python Process Injection Proof of Concept Code
=========================

Proof of Concept code written to demonstrate using python-ptrace to inject code into arbritary processes on Linux
for my talk at [SteelCon] in July 2014.

Dependencies:
----
* [python-paramiko] (for DiabolicalMouse-mass.py stager utility)
* [python-ptrace] (for injection tools)

Licence:
----
See LICENCE.txt - uses the WTFPL licence.

What?
----
* x86-inject.py - Simple x86 process injection tool for demonstration purposes.
* x64-inject.py - Simple x86_64 process injection tool for demonstration purposes.
* x64-inject-fork.py - Simple x86_64 process injection tool for demonstration purposes, which prepends the shellcode with a "fork" call in the hopes of not harming target process.
* armv7l-inject.py - Simple ARMv7l process injection tool for demonstration purposes. (missing, somewhere on my Nexus 7...)
* EnchantedMushroom.py - Multi Arch (ARMv7l, x86, x86_64) process injection tool which intelligently detects which architecture it is running on, and deploys the correct shellcode/technique as-needed
* DiabolicalMouse-mass.py - Automatic stager for deploying python scripts in-memory across multiple hosts using SSH. 

Author
----
Darren Martyn

Contact:
----
Best way is probably twitter - [@info_dox]

Thanks
----
Many thanks to the [SteelCon] crew for giving me a chance to present this, and also to my colleagues at [Xiphos Research Labs] who helped me out with presenting it and testing out the code.

Also thanks to [jtripper], [elfmaster], and the various authors of [Phrack] articles that helped me get the idea solid in my head and understand what I was trying to do with their sample code and srticles and such


[SteelCon]:http://www.steelcon.info/
[python-paramiko]:http://www.paramiko.org/en/latest/
[python-ptrace]:http://python-ptrace.readthedocs.org/en/latest/
[@info_dox]:https://twitter.com/info_dox
[Xiphos Research Labs]:http://www.xiphosresearch.com/
[jtripper]:https://github.com/jtripper
[elfmaster]:http://bitlackeys.org/
[Phrack]:http://phrack.org/
