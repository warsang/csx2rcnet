Just a small python script that allows to convert cheat engine csx structure files to rcnet format (importable in reclass .NET)

Both tools are great, this just allows to work from one format to another.


## Usage
Reverse engineer your structure with Cheat-Engine, (in my case, I was using cake-san's UE4 plugin https://fearlessrevolution.com/viewtopic.php?t=14414)

From the struct dissector, export the struct to a .CTX file

In the python script change the 
```
tree = ET.parse(r"C:\<PATHTOSTRUCTUREFILE>.CSX")
```

to the path to your .ctx file;

Run the script.

You'll have to pass the base address for all your structs as these are not in the .CTX file but are needed for ReClass

I started working on the rcnet2csx.py equivalent but haven't finished it.

## FAQ

* Could this be a C# ReClass plugin?
Yes, this could be a ReClass C# plugin

