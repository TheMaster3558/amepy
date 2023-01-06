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

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, TypeVar, Optional, Union

import aiohttp

from .enums import HypesquadHouse, Orientation, TrinityType, VersusColors
from .utils import json_or_data, raise_http_errors, MISSING

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, Self

    P = ParamSpec('P')


T = TypeVar('T')


class Client:
    """
    A client used for interacting with the **Améthyste API**

    Examples
    --------
    Write data to file

    .. code:: py

        import asyncio
        import pyame

        async def main():
            async with pyame.Client('api_key') as client:
                data = await client.triggered('image_url')
                with open('triggered.gif', 'wb') as f:
                    f.write(data)

        asyncio.run(main())

    Send data through discord bot (doesn't use files)

    .. code:: py

        import asyncio
        import io
        import pyame

        import discord
        from discord.ext import commands

        class MyBot(commands.Bot):
            async def setup_hook():
                self.client = pyame.Client('api_key')
                await self.client.create_session()

            async def close():
                await self.client.close()
                await super().close()

        bot = MyBot(...)

        @bot.hybrid_command()
        async def crush(ctx, member: discord.Member):
            data = await ctx.bot.client.crush(member.display_avatar.url)
            buffer = io.BytesIO(data)
            file = discord.File(buffer)
            await ctx.send(file=file)

        bot.run(...)

    |

    .. container:: operations

       .. describe:: async with x

           Asynchronously initialises the client and automatically cleans up.

    |

    .. note::

        All methods that return bytes can be written to a binary file (png or gif) to view the output

    |

    Parameters
    ----------
    api_key: class:`str`
        The api key to use, receive one `here <https://api.amethyste.moe/>`_


    |
    """

    _BASE: ClassVar[str] = 'https://v1.api.amethyste.moe'

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key
        self.session: Optional[aiohttp.ClientSession] = None

    async def create_session(self) -> None:
        """
        This method is used to initialise the client
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self) -> None:
        """
        This method is used to close the client
        """
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def __aenter__(self) -> Self:
        await self.create_session()
        return self

    async def __aexit__(self, *exc_args: Any) -> None:
        await self.close()

    @property
    def headers(self) -> Dict[str, str]:
        return {'Authorization': f'Bearer {self.api_key}'}

    async def _request(self, method: str, endpoint: str, /, **json: Any) -> Union[Dict[str, Any], bytes]:
        assert self.session is not None
        async with self.session.request(method, self._BASE + endpoint, json={k: v for k, v in json.items() if v is not MISSING}, headers=self.headers) as response:
            data = await json_or_data(response)
            raise_http_errors(data, response.status)
            return data

    async def _generate_request(self, name: str, **json: Any) -> bytes:
        data = await self._request('POST', '/generate/' + name, **json)
        assert isinstance(data, bytes)
        return data

    async def get_free_endpoints(self) -> List[str]:
        """
        Returns
        -------
        :class:`List[str]`
        """
        data = await self._request('GET', '/generate')
        assert isinstance(data, dict)
        return data['endpoints']['free']

    async def get_premium_endpoints(self) -> List[str]:
        """
        Returns
        -------
        :class:`List[str]`
        """
        data = await self._request('GET', '/generate')
        assert isinstance(data, dict)
        return data['endpoints']['premium']

    async def get_random_wallpaper(self) -> str:
        """
        Returns
        -------
        :class:`str` The url of the wallpaper
        """
        data = await self._request('GET', '/image/wallpaper')
        assert isinstance(data, dict)
        return data['url']
    
    async def three_thousand_years(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('3000years', url=image_url)

    async def approved(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('approved', url=image_url)

    async def afusion(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('afusion', url=image_url)

    async def badge(self, avatar_url: str, *, username: str, servers: int, users: int) -> bytes:
        """
        Parameters
        ----------
        avatar_url: :class:`str`
            The url of the avatar to use
        username: :class:`str`
            The username to use in the badge
        servers: :class:`int`
            The amount of servers to show in the badge
        users: :class:`int`
            The amount of users to show in the madge


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('badge', url=avatar_url, text=username, numberserver=servers, numberusers=users)

    async def batslap(self, image_url: str, target_image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        target_image_url: :class:`str`
            The url of the target image

        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('batslap', avatar=image_url, url=target_image_url)

    async def beautiful(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('beuautiful', url=image_url)

    async def blur(self, image_url: str, *, amount: int = MISSING) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        amount: :class:`int`
            The amount of blue to use (defaults to 5)


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('blur', url=image_url, blur=amount)

    async def blurple(self, image_url: str, *, invert: bool = MISSING) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        invert: :class:`bool`
            Whether to invert the colors of the image


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('blurple', url=image_url, invert=invert)

    async def brazzers(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('brazzers', url=image_url)

    async def burn(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('burn', url=image_url)

    async def challenger(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('challenger', url=image_url)

    async def circle(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('circle', url=image_url)

    async def constrast(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('contrast', url=image_url)

    async def crush(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('crush', url=image_url)

    async def facebook(self, image_url: str, *, text: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        text: class:`str`
            The text in the facebook post


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('facebook', url=image_url, text=text)    

    async def ddungeon(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('ddungeon', url=image_url)

    async def deepfry(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('deepfry', url=image_url)

    async def dictator(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('dictator', url=image_url) 

    async def discord_house(self, image_url: str, *, hypequad_house: HypesquadHouse) -> bytes:
        return await self._generate_request('discordhouse', url=image_url, house=hypequad_house.
                                            value)

    async def distort(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('distort', url=image_url)

    async def dither565(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('dither565', url=image_url)

    async def emboss(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('emboss', url=image_url) 

    async def fire(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('fire', url=image_url)

    async def frame(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('frame', url=image_url)

    async def gay(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('gay', url=image_url)

    async def glitch(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('glitch', url=image_url)

    async def greyple(self, image_url: str, *, invert: bool = MISSING) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        invert: :class:`bool`
            Whether to invert the colors of the image


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('greyple', url=image_url, invert=invert)

    grayple = greyple

    async def greyscale(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('greyscale', url=image_url)

    grayscale = greyscale

    async def instagram(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('instagram', url=image_url)

    async def invert(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('invert', url=image_url)

    async def jail(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('jail', url=image_url)

    async def look_what_karen_have(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('lookwhatkarenhave', url=image_url)

    async def magik(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('magik', url=image_url)

    async def mission_passed(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('missionpassed', url=image_url)

    async def moustache(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('moustache', url=image_url)

    async def pixelize(self, image_url: str, amount: int = MISSING) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        amount: :class:`int`
            The amount to pixelize (default to 5, minimum of 1, maximum of 50)


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('pixelize', url=image_url, pixelize=amount)

    async def playstation_four(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('ps4', url=image_url)

    async def posterize(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('posterize', url=image_url)

    async def rejected(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('rejected', url=image_url)

    async def redple(self, image_url: str, *, invert: bool = MISSING) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        invert: :class:`bool`
            Whether to invert the colors of the image


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('redple', url=image_url, invert=invert)

    async def rest_in_peace(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('rip', url=image_url)

    async def scary(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('scary', url=image_url)

    async def sepia(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('sepia', url=image_url)

    async def sharpen(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('sharpen', url=image_url)

    async def sniper(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('sniper', url=image_url)

    async def steam_card(self, image_url: str, *, text: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        text: class:`str`
            The text to put on the card


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('steamcard', url=image_url, text=text)

    async def symmetry(self, image_url: str, *, orientation: Orientation) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        orientation: :class:`Orientation`
            The orientation to apply the symmetry on


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('symmetry', url=image_url, orientation=orientation.value)
    
    async def thanos(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('thanos', url=image_url)

    async def trinity(self, image_url: str, *, type: TrinityType) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        type: class:`TrinityType`
            The type of image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('trinity', url=image_url, type=type.
                                            value)

    async def to_be_continued(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('tobecontinued', url=image_url)

    async def twitter(self, image_url: str, avatar1: str, avatar2: str, avatar3: str, *, text: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        avatar1: class:`str`
            The url of the first bottom avatar
        avatar2: class:`str`
            The url of the second bottom avatar
        avatar3: class:`str`
            The url of the third bottom avatar
        text: class:`str`
            The text in the tweet


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('twitter', url=image_url, avatar1=avatar1, avatar2=avatar2, avatar3=avatar3, text=text)

    async def spin(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('spin', url=image_url)

    async def subzero(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('subzero', url=image_url)

    async def triggered(self, image_url: str, *, blur: bool = MISSING, greyscale: bool = MISSING, grayscale: bool = MISSING, horizontal: bool = MISSING, invert: bool = MISSING, sepia: bool = MISSING, vertical: bool = MISSING) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use
        blur: :class:`bool`
            Whether to blur the gif
        greyscale: :class:`bool`
            Whether to convert the gif to greyscale
        grayscale: class:`bool`
            Alias to `greyscale`
        horizontal: :class:`bool`
            Effect of this parameter is unknown
        invert: :class:`bool`
            Whether to invert the colors of the image
        sepia: class:`bool`
            Whether to apply a sepia filter on the gif
        vertical: :class:`bool`
            Effect of this parameter is unknown


        Returns
        -------
        A :class:`bytes` that represents the data of the gif
        """
        if greyscale is not MISSING and grayscale is not MISSING:
            raise TypeError('greyscale and grayscale cannot both be provided')
        greyscale = grayscale if grayscale is not MISSING else greyscale
        return await self._generate_request('triggered', url=image_url, blue=blur, greyscale=greyscale, horizontal=horizontal, invert=invert, sepia=sepia, veritical=vertical)

    async def unsharpen(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('unsharpen', url=image_url)

    async def ultimate_tattoo(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('utatoo', url=image_url)

    async def versus(self, left_image_url: str, right_image_url: str, *, color: VersusColors) -> bytes:
        """
        Parameters
        ----------
        left_image_url: :class:`str`
            The url of the image to use on the left side
        right_image_url: :class:`str`
            The url of the image to use on the right side
        color: :class:`VersusColors`
            The color combination to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('vs', url=left_image_url, avatar=right_image_url, type=color.value)

    async def wanted(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('wanted', url=image_url)

    async def wasted(self, image_url: str) -> bytes:
        """
        Parameters
        ----------
        image_url: :class:`str`
            The url of the image to use


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('wasted', url=image_url)

    async def who_would_win(self, left_image_url: str, right_image_url: str) -> bytes:
        """
        Parameters
        ----------
        left_image_url: :class:`str`
            The url of the image to use on the left side
        right_image_url: :class:`str`
            The url of the image to use on the right side


        Returns
        -------
        A :class:`bytes` that represents the data of the png image
        """
        return await self._generate_request('whowouldwin', url=left_image_url, avatar=right_image_url)
