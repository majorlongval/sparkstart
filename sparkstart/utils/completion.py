"""Shell completion support for bash and zsh."""

import pathlib


def generate_bash_completion() -> str:
    """Generate bash completion script."""
    return r'''
_sparkstart_completion() {
    local cur prev words cword
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    words=("${COMP_WORDS[@]}")
    cword=$COMP_CWORD

    # Main commands
    local commands="new help version"

    # For 'sparkstart' or 'sparkstart <command>'
    if [[ $cword -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "$commands" -- "$cur") )
        return 0
    fi

    # Options for 'new' command
    if [[ "${words[1]}" == "new" ]]; then
        if [[ "$cur" == -* ]]; then
            local options="--github --lang --template --tutorial --devcontainer --tools --help"
            COMPREPLY=( $(compgen -W "$options" -- "$cur") )
            return 0
        fi

        # Complete language values
        if [[ "$prev" == "--lang" ]] || [[ "$prev" == "-l" ]]; then
            COMPREPLY=( $(compgen -W "python rust javascript cpp" -- "$cur") )
            return 0
        fi

        # Complete template values
        if [[ "$prev" == "--template" ]]; then
            COMPREPLY=( $(compgen -W "pygame" -- "$cur") )
            return 0
        fi
    fi

    return 0
}

complete -o bashdefault -o default -o nospace -F _sparkstart_completion sparkstart
'''.strip()


def generate_zsh_completion() -> str:
    """Generate zsh completion script."""
    return r'''
#compdef sparkstart

_sparkstart() {
    local -a commands
    commands=(
        'new:Create a new project (interactive wizard or direct mode)'
        'help:Show help information'
        'version:Show version'
    )

    _arguments -S \
        '(- *)'{-h,--help}'[Show help]' \
        '(- *)'{-v,--version}'[Show version]' \
        '(-): :->command' \
        '(-)*:: :->args'

    case $state in
        command)
            _describe 'sparkstart commands' commands
            ;;
        args)
            case ${words[2]} in
                new)
                    _arguments \
                        '(-g --github)'{-g,--github}'[Push to GitHub]' \
                        '(-l --lang)'{-l,--lang}'[Language]:language:(python rust javascript cpp)' \
                        '--template[Project template]:template:(pygame)' \
                        '(-t --tutorial)'{-t,--tutorial}'[Create educational game project]' \
                        '(-d --devcontainer)'{-d,--devcontainer}'[Generate dev container config]' \
                        '--tools[Include code quality tools]' \
                        '(-h --help)'{-h,--help}'[Show help]'
                    ;;
            esac
            ;;
    esac
}

_sparkstart
'''.strip()


def install_completion(shell: str = "bash") -> None:
    """Install shell completion to user's shell config."""
    home = pathlib.Path.home()

    if shell == "bash":
        completion_script = generate_bash_completion()
        config_file = home / ".bashrc"
        completion_marker = "# sparkstart bash completion"
    elif shell == "zsh":
        completion_script = generate_zsh_completion()
        config_file = home / ".zshrc"
        completion_marker = "# sparkstart zsh completion"
    else:
        raise ValueError(f"Unsupported shell: {shell}")

    if not config_file.exists():
        config_file.touch()

    config_content = config_file.read_text()

    # Check if already installed
    if completion_marker in config_content:
        return  # Already installed

    # Add completion to config
    completion_line = f'{completion_marker}\neval "$(sparkstart --{shell}-completion)"'
    config_content += f"\n\n{completion_line}\n"
    config_file.write_text(config_content)
