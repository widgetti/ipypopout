from contextlib import contextmanager
from ipywidgets.widgets.widget import _remove_buffers, _show_traceback, _put_buffers


class SyncPatchMixin:
    """Mixin to patch widget state sync in case a widget is displayedi in multiple windows.
    See: https://github.com/jupyter-widgets/ipywidgets/issues/3111 and
    https://github.com/maartenbreddels/ipywidgets/commit/eaf9a4f6e3d4ec3ebe2d041179458411727e2596"""
    _holding_sync_from_frontend_update = False

    def send_state(self, key=None):
        state = self.get_state(key=key)
        if len(state) > 0:
            state, buffer_paths, buffers = _remove_buffers(state)
            msg = {'method': 'update', 'state': state, 'buffer_paths': buffer_paths}
            self._send(msg, buffers=buffers)

    def set_state(self, sync_data):
        with self._hold_sync_frontend(), self.hold_trait_notifications():
            for name in sync_data:
                if name in self.keys:
                    from_json = self.trait_metadata(name, 'from_json',
                                                    self._trait_from_json)
                    self.set_trait(name, from_json(sync_data[name], self))

    def notify_change(self, change):
        name = change['name']
        if self.comm is not None and self.comm.kernel is not None and name in self.keys:
            if self._holding_sync:
                # if we're holding a sync, we will only record which trait was changed
                # but we skip those traits marked no_echo, during an update from the frontend
                if not (self._holding_sync_from_frontend_update
                        and self.trait_metadata(name, 'no_echo')):
                    self._states_to_send.add(name)
            else:
                # otherwise we send it directly
                self.send_state(key=name)
        super().notify_change(change)

    @contextmanager
    def _hold_sync_frontend(self):
        if self._holding_sync_from_frontend_update is True:
            with self.hold_sync():
                yield
        else:
            try:
                self._holding_sync_from_frontend_update = True
                with self.hold_sync():
                    yield
            finally:
                self._holding_sync_from_frontend_update = False

    @_show_traceback
    def _handle_msg(self, msg):
        data = msg['content']['data']
        method = data['method']

        if method == 'update':
            if 'state' in data:
                state = data['state']
                if 'buffer_paths' in data:
                    _put_buffers(state, data['buffer_paths'], msg['buffers'])
                self.set_state(state)

        # Handle a state request.
        elif method == 'request_state':
            self.send_state()

        # Handle a custom msg from the front-end.
        elif method == 'custom':
            if 'content' in data:
                with self._hold_sync_frontend():
                    self._handle_custom_msg(data['content'], msg['buffers'])

        # Catch remainder.
        else:
            self.log.error('Unknown front-end to back-end widget msg with method "%s"' % method)
