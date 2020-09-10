from abc import abstractmethod, ABCMeta

import pt3.state as state


class Layout(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, desk):
        self.desk = desk  # Should never change
        self.active = False
        self.tiling = False

    @abstractmethod
    def add(self, c):
        pass

    @abstractmethod
    def remove(self, c):
        pass

    @abstractmethod
    def tile(self, save=True):
        if not self.active or self.desk not in state.visible_desktops:
            return False

        if not self.tiling and save:
            for c in self.clients():
                c.save()
        #                c.unmaximize()

        for c in self.clients():  # unmaximize all windows while tiling
            c.unmaximize()
        self.tiling = True

        return True

    @abstractmethod
    def untile(self):
        pass

    @abstractmethod
    def next_client(self):
        pass

    @abstractmethod
    def switch_next_client(self):
        pass

    @abstractmethod
    def prev_client(self):
        pass

    @abstractmethod
    def switch_prev_client(self):
        pass

    @abstractmethod
    def clients(self):
        pass

    def get_workarea(self):
        if self.desk not in state.visible_desktops:
            return None

        mon = state.work_area[state.visible_desktops.index(self.desk)]

        return mon

    def __str__(self):
        wa = self.get_workarea()
        if wa is None:
            wastr = 'which isn\'t visible'
        else:
            wx, wy, ww, wh = wa
            wastr = '%dx%d+%d+%d' % (ww, wh, wx, wy)

        istiling = '- TILING' if self.tiling else ''

        return '%s (desk %d) %s%s' % (
            self.__class__.__name__, self.desk, wastr, istiling)


from .layout_vert_horz import VerticalLayout, HorizontalLayout

layouts = [VerticalLayout, HorizontalLayout]
