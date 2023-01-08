"""
MIT License

Copyright (c) 2022-present TheMaster3558

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
from typing import Any, ClassVar, Dict, Union, Optional, Type


class HTTPException(Exception):
    status: ClassVar[int] = -1

    def __init__(self, data: Union[Dict[str, Any], bytes]) -> None:
        self.data: Dict[str, Any] = data if isinstance(data, dict) else json.loads(data.decode())
        super().__init__(f'{self.status} {self.message}')

    @property
    def message(self) -> Optional[str]:
        return self.data.get('message')


class BadRequest(HTTPException):
    status = 400


class Unauthorized(HTTPException):
    status = 401


class Forbidden(HTTPException):
    status = 403


class NotFound(HTTPException):
    status = 404


class PayloadTooLarge(HTTPException):
    status = 413


class InternalServerError(HTTPException):
    status = 500


class NotImplemented(HTTPException):
    status = 501


class BadGateway(HTTPException):
    status = 502


class ServiceUnavailiable(HTTPException):
    status = 503


error_mapping: Dict[int, Type[HTTPException]] = {cls.status: cls for cls in globals().values() if isinstance(cls, type) and issubclass(cls, HTTPException)}
