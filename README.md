(This is a fork of https://github.com/BurntSushi/pytyle3 which tries to port pytyle3 to Python 3)

An updated (and much faster) version of pytyle that uses xpybutil and is
compatible with Openbox Multihead.

Due to using xpybutil much of the lower level XCB/xpyb stuff has been factored 
out of pytyle3. Also, because it relies on Openbox Multihead when there is more 
than one monitor active, a lot less state needs to be saved.

As a result, pytyle3 is ~1000 lines while pytyle2 is ~7000 lines. Additionally, 
because of a simpler design, pytyle3's memory footprint is much smaller and is 
actually quite snappier in moving windows on the screen.

# Installation
It should be as straight-forward as

```python
sudo python3 setup.py install
```

Two configuration files, config.py and keybind.py will be copied to 
/etc/xdg/pytyle3.

To configure pytyle3 on a user basis, create ~/.config/pytyle3 and copy 
/etc/xdg/pytyle3/*py to that directory.

pytyle3 will require a restart if the configuration has changed.
