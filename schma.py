def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    # 🔧 Remove `null` from optional query params
    for path in schema["paths"].values():
        for method in path.values():
            for param in method.get("parameters", []):
                schema_def = param.get("schema", {})
                if "anyOf" in schema_def:
                    schema_def.pop("anyOf", None)
                    schema_def.pop("nullable", None)
                    schema_def["type"] = "integer"

    app.openapi_schema = schema
    return app.openapi_schema
