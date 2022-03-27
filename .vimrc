set nocompatible              " be iMproved, required
filetype off                  " required

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'
Plugin 'flazz/vim-colorschemes'
Plugin 'scrooloose/nerdtree'
Plugin 'jistr/vim-nerdtree-tabs'
Plugin 'Valloric/YouCompleteMe'
Plugin 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' } 
Plugin 'junegunn/fzf.vim'
" Plugin 'kien/ctrlp.vim'
" Plugin 'tacahiroy/ctrlp-funky'
Plugin 'majutsushi/tagbar'
Plugin 'mileszs/ack.vim'
Plugin 'tomtom/tcomment_vim'
Plugin 'airblade/vim-gitgutter'

call vundle#end()            " required
filetype plugin indent on    " required

" NERDTreeToggle
nnoremap <c-a> : NERDTreeToggle<CR>
nnoremap <F8> : TagbarToggle<CR>
let g:tagbar_width = 30
" autocmd BufReadPost *.py call tagbar#autoopen() 

syntax enable

set nu
set t_Co=256
set cursorline
set background=dark
"colorscheme molokai
colorscheme gruvbox
"colorscheme wombat

" Use highlighting when doing a search.
set hlsearch 
set path=.,/usr/include,,**

" Set tab width to 4 columns.
set tabstop=4
set expandtab
set autoindent

map <C-s> :call SwitchLineNumber()<CR>
map! <C-s> <Esc>:call SwitchLineNumber()<CR>
function SwitchLineNumber()
    if (&nu == 0)
        set nu
        echo "Enable line number."
    else
        set nonu
        echo "Disable line number."
    endif
endfunction

"ctrl+o Support mouse
map <C-o> :call SwitchMouseMode()<CR>
map! <C-o> <Esc>:call SwitchMouseMode()<CR>
function SwitchMouseMode()
    if (&mouse == "a")
        let &mouse = ""
        echo "Mouse is disabled."
    else
        let &mouse = "a"
        echo "Mouse is enabled."
    endif
endfunction

" Runnung code F5 setting
nmap <F5> :call CompileRun()<CR>
func! CompileRun()
        exec "w"
if &filetype == 'python'
            exec "!time python3 %"
endif
    endfunc

" JSON format setting
command! JSONFormat :execute '%!python3 -m json.tool'

" YouCompleteMe
let g:ycm_global_ycm_extra_conf='~/.vim/bundle/YouCompleteMe/.ycm_extra_conf.py'
let g:ycm_confirm_extra_conf=0
let g:ycm_python_binary_path='/usr/bin/python3'

"" CtrlP
"let g:ctrlp_map = '<c-p>'
"let g:ctrlp_cmd = 'CtrlP'
"let g:ctrlp_working_path_mode = 'ra'
"let g:ctrlp_custom_ignore = {
"  \ 'dir':  '\v[\/]\.(git|hg|svn)$',
"  \ 'file': '\v\.(exe|so|dll)$',
"  \ 'link': 'some_bad_symbolic_links',
"  \ }
"
"" The Silver Searcher
"if executable('ag')
"  " Use ag over grep
"  set grepprg=ag\ --nogroup\ --nocolor
"  " Use ag in CtrlP for listing files. Lightning fast and respects .gitignore
"  let g:ctrlp_user_command = 'ag %s -l --nocolor -g ""'
"  " ag is fast enough that CtrlP doesn't need to cache
"  let g:ctrlp_use_caching = 0
"endif

" fzf settings
" This is the default extra key bindings
nnoremap ff :Files<CR>
nnoremap fa :Ag<CR>
let g:fzf_action = {
            \ 'ctrl-t': 'tab split',
            \ 'ctrl-x': 'split',
            \ 'ctrl-v': 'vsplit' }

" Customize fzf colors to match your color scheme
let g:fzf_colors =
            \ { 'fg':      ['fg', 'Normal'],
            \ 'bg':      ['bg', 'Normal'],
            \ 'hl':      ['fg', 'Comment'],
            \ 'fg+':     ['fg', 'CursorLine', 'CursorColumn', 'Normal'],
            \ 'bg+':     ['bg', 'CursorLine', 'CursorColumn'],
            \ 'hl+':     ['fg', 'Statement'],
            \ 'info':    ['fg', 'PreProc'],
            \ 'prompt':  ['fg', 'Conditional'],
            \ 'pointer': ['fg', 'Exception'],
            \ 'marker':  ['fg', 'Keyword'],
            \ 'spinner': ['fg', 'Label'],
            \ 'header':  ['fg', 'Comment'] }

" explicitly bind the keys to down and up in your $FZF_DEFAULT_OPTS.
let g:fzf_history_dir = '~/.local/share/fzf-history'


"Ack
if executable('ag')
  let g:ackprg = 'ag --vimgrep'
endif
nnoremap FF :Ack!<Space>

" Vim-gitgutter
set updatetime=100
highlight GitGutterAdd    ctermfg=blue
highlight GitGutterChange ctermfg=green
highlight GitGutterDelete ctermfg=red
