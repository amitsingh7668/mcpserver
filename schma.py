    for path in schema["paths"].values():
        for method in path.values():
            for param in method.get("parameters", []):
                schema_def = param.get("schema", {})

                if "anyOf" in schema_def:
                    # extract the non-null schema
                    non_null = next(
                        (s for s in schema_def["anyOf"] if s.get("type") != "null"),
                        None,
                    )

                    if non_null:
                        schema_def.clear()
                        schema_def.update(non_null)

    app.openapi_schema = schema
    return app.openapi_schema
