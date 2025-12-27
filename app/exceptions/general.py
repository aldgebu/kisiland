from fastapi import FastAPI, Request, status

from starlette.responses import JSONResponse


class UnauthorizedException(Exception):
    def __init__(self, message: str = 'Invalid username or password.'):
        self.message = message
        super().__init__(self.message)


class NotFoundException(Exception):
    def __init__(self, data_name: str):
        self.message = f'{data_name} not found.'


class MembershipVisitsLimitReachedException(Exception):
    def __init__(self):
        self.message = 'Membership visits limit reached.'


class UnlimitedVisitPricingException(Exception):
    def __init__(self, actual_price: float, payed_amount: float):
        self.message = f'Unlimited visit price is {actual_price}, but {payed_amount} was payed!'


def register_exceptions(app: FastAPI):
    @app.exception_handler(Exception)
    async def handle_exceptions(
        request: Request,
        exc: Exception
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'error': 'Internal Server Error',
                'message': 'Call ALDGEBU!'
            }
        )

    @app.exception_handler(UnauthorizedException)
    async def handle_unauthorized_exception(
        request: Request,
        exc: UnauthorizedException
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'error': 'Unauthorized',
                'message': exc.message
            }
        )

    @app.exception_handler(NotFoundException)
    async def handle_not_found_exception(
        request: Request,
        exc: NotFoundException
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'error': 'Not found',
                'message': exc.message
            }
        )

    @app.exception_handler(MembershipVisitsLimitReachedException)
    async def handle_membership_visits_limit_reached_exception(
        request: Request,
        exc: MembershipVisitsLimitReachedException
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'error': 'Limit reached',
                'message': exc.message
            }
        )

    @app.exception_handler(UnlimitedVisitPricingException)
    async def handle_unlimited_visit_pricing_exception(
        request: Request,
        exc: UnlimitedVisitPricingException
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'error': 'Unlimited visit pricing',
                'message': exc.message
            }
        )
