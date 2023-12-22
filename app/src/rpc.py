from aiohttp import web

async def eval_payload(prompt: str, aio: bool) -> str:
    if aio:
        try:
            return await eval(prompt)
        except:
            return None

    try:
        return eval(prompt)
    except:
        return None


async def exec_payload(prompt: str, aio: bool) -> None:
    if aio:
        try:
            await exec(prompt)
        except:
            pass

    try:
        exec(prompt)
    except:
        pass


async def evalRPC(request) -> web.Response:
    payload = await request.json()

    if "eval" in payload.keys():
        try:
            evaluated_res = await eval_payload(
                prompt=payload["eval"][">>>"],
                aio=payload["eval"]["async"]
            )
        except Exception as e:
            return web.json_response(
                {
                    "status": False,
                    "log": "Not Evaluated",
                    "code": 1,
                    f"Exception {e}": {
                        "name": str(e),
                        "args": e.args,
                    }
                }
            )

    if "exec" in payload.keys():
        try:
            _ = await exec_payload(
                prompt=payload["exec"][">>>"],
                aio=payload["exec"]["async"]
            )
        except Exception as e:
            return web.json_response(
                {
                    "status": False,
                    "log": "Not Excuted",
                    "code": 2,
                    f"Exception {e}": {
                        "name": str(e),
                        "args": e.args,
                    }
                }
            )

    return web.json_response(
        {
            "status": True,
            "log": "sucess",
            "code": 0,
            "evaluated": evaluated_res
        }
    )
