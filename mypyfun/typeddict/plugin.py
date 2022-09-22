from mypy.plugin import Plugin
from mypy.plugin import AnalyzeTypeContext
from typing import Optional, Callable

from mypy.types import AnyType, Type, TypeOfAny, TypedDictType


class TypedDictExtensionsPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str) -> Optional[Callable[[AnalyzeTypeContext], Type]]:
        if fullname == "mypyfun.typeddict.types.Partial":
            return self._partial_dict_type_analyze_hook
        elif fullname == "mypyfun.typeddict.types.Required":
            return self._required_dict_type_analyze_hook
        elif fullname == "mypyfun.typeddict.types.Omit":
            return self._omit_type_analyze_hook
        elif fullname == "mypyfun.typeddict.types.Pick":
            return self._pick_type_analyze_hook

    def _check_params(self, name: str, ctx: AnalyzeTypeContext, with_args: bool = False) -> tuple[Optional[TypedDictType], list[str]]:
        # Should have single arg, and should be a TypedDict

        if len(ctx.type.args) == 0:
            ctx.qpi.fail(f'{name} requires at least a TypeDict parameter')
            return None, []

        if  not with_args and len(ctx.type.args) > 1:
            ctx.api.fail(f'{name} only takes one paramater of type TypeDict', ctx=ctx.context)
            return None, []

        args = []
        if with_args:
            for arg in ctx.type.args[1:]:
                args.append(arg.name)

        arg_type = ctx.api.analyze_type(ctx.type.args[0])

        if not isinstance(arg_type, TypedDictType):
            ctx.api.fail(f"{name} can only be applied to TypedDict", ctx=ctx.context)
            return None, []

        return arg_type, args

    def _partial_dict_type_analyze_hook(self, ctx: AnalyzeTypeContext) -> Type:
        type_param, _  = self._check_params('PartialDict', ctx)

        if type_param is None:
            return AnyType(TypeOfAny.from_error)

        # Return a copy of the TypeDict with no required_keys
        return type_param.copy_modified(required_keys=set())


    def _required_dict_type_analyze_hook(self, ctx: AnalyzeTypeContext) -> Type:
        type_param, _  = self._check_params('RequiredDict', ctx)

        if type_param is None:
            return AnyType(TypeOfAny.from_error)

        # Return a copy of TypedDict with all keys mandatory
        # assert isinstance(type_param, TypedDictType)
        return type_param.copy_modified(required_keys=set(type_param.items.keys()))


    def _omit_type_analyze_hook(self, ctx: AnalyzeTypeContext) -> Type:
        type_param, args = self._check_params('Omit', ctx, with_args=True)

        items = {k: v for k, v in type_param.items.items() if k not in args}
        required_keys = {k for k in type_param.required_keys if k not in args}

        return TypedDictType(items, required_keys, type_param.fallback, type_param.line, type_param.column)

    def _pick_type_analyze_hook(self, ctx: AnalyzeTypeContext) -> Type:
        type_param, args = self._check_params('Omit', ctx, with_args=True)

        items = {k: v for k, v in type_param.items.items() if k in args}
        required_keys = {k for k in type_param.required_keys if k in args}

        return TypedDictType(items, required_keys, type_param.fallback, type_param.line, type_param.column)


def plugin(version: str) -> Plugin:
    return TypedDictExtensionsPlugin

