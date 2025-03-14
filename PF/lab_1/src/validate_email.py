def validate_email(arg):
    return arg.count('@')>0 and arg.count('.')>0
