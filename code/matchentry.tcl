
if {![info exists vTcl(sourcing)]} {

    package require Tk
    switch $tcl_platform(platform) {
    windows {
            option add *Button.padY 0
    }
    default {
            option add *Scrollbar.width 10
            option add *Scrollbar.highlightThickness 0
            option add *Scrollbar.elementBorderWidth 2
            option add *Scrollbar.borderWidth 2
    }
    }
    
}

#############################################################################
# Visual Tcl v1.60 Project
#


#################################
# VTCL LIBRARY PROCEDURES
#

if {![info exists vTcl(sourcing)]} {
#############################################################################
## Library Procedure:  Window

proc ::Window {args} {
    ## This procedure may be used free of restrictions.
    ##    Exception added by Christian Gavin on 08/08/02.
    ## Other packages and widget toolkits have different licensing requirements.
    ##    Please read their license agreements for details.

    global vTcl
    foreach {cmd name newname} [lrange $args 0 2] {}
    set rest    [lrange $args 3 end]
    if {$name == "" || $cmd == ""} { return }
    if {$newname == ""} { set newname $name }
    if {$name == "."} { wm withdraw $name; return }
    set exists [winfo exists $newname]
    switch $cmd {
        show {
            if {$exists} {
                wm deiconify $newname
            } elseif {[info procs vTclWindow$name] != ""} {
                eval "vTclWindow$name $newname $rest"
            }
            if {[winfo exists $newname] && [wm state $newname] == "normal"} {
                vTcl:FireEvent $newname <<Show>>
            }
        }
        hide    {
            if {$exists} {
                wm withdraw $newname
                vTcl:FireEvent $newname <<Hide>>
                return}
        }
        iconify { if $exists {wm iconify $newname; return} }
        destroy { if $exists {destroy $newname; return} }
    }
}
#############################################################################
## Library Procedure:  vTcl:DefineAlias

proc ::vTcl:DefineAlias {target alias widgetProc top_or_alias cmdalias} {
    ## This procedure may be used free of restrictions.
    ##    Exception added by Christian Gavin on 08/08/02.
    ## Other packages and widget toolkits have different licensing requirements.
    ##    Please read their license agreements for details.

    global widget
    set widget($alias) $target
    set widget(rev,$target) $alias
    if {$cmdalias} {
        interp alias {} $alias {} $widgetProc $target
    }
    if {$top_or_alias != ""} {
        set widget($top_or_alias,$alias) $target
        if {$cmdalias} {
            interp alias {} $top_or_alias.$alias {} $widgetProc $target
        }
    }
}
#############################################################################
## Library Procedure:  vTcl:DoCmdOption

proc ::vTcl:DoCmdOption {target cmd} {
    ## This procedure may be used free of restrictions.
    ##    Exception added by Christian Gavin on 08/08/02.
    ## Other packages and widget toolkits have different licensing requirements.
    ##    Please read their license agreements for details.

    ## menus are considered toplevel windows
    set parent $target
    while {[winfo class $parent] == "Menu"} {
        set parent [winfo parent $parent]
    }

    regsub -all {\%widget} $cmd $target cmd
    regsub -all {\%top} $cmd [winfo toplevel $parent] cmd

    uplevel #0 [list eval $cmd]
}
#############################################################################
## Library Procedure:  vTcl:FireEvent

proc ::vTcl:FireEvent {target event {params {}}} {
    ## This procedure may be used free of restrictions.
    ##    Exception added by Christian Gavin on 08/08/02.
    ## Other packages and widget toolkits have different licensing requirements.
    ##    Please read their license agreements for details.

    ## The window may have disappeared
    if {![winfo exists $target]} return
    ## Process each binding tag, looking for the event
    foreach bindtag [bindtags $target] {
        set tag_events [bind $bindtag]
        set stop_processing 0
        foreach tag_event $tag_events {
            if {$tag_event == $event} {
                set bind_code [bind $bindtag $tag_event]
                foreach rep "\{%W $target\} $params" {
                    regsub -all [lindex $rep 0] $bind_code [lindex $rep 1] bind_code
                }
                set result [catch {uplevel #0 $bind_code} errortext]
                if {$result == 3} {
                    ## break exception, stop processing
                    set stop_processing 1
                } elseif {$result != 0} {
                    bgerror $errortext
                }
                break
            }
        }
        if {$stop_processing} {break}
    }
}
#############################################################################
## Library Procedure:  vTcl:Toplevel:WidgetProc

proc ::vTcl:Toplevel:WidgetProc {w args} {
    ## This procedure may be used free of restrictions.
    ##    Exception added by Christian Gavin on 08/08/02.
    ## Other packages and widget toolkits have different licensing requirements.
    ##    Please read their license agreements for details.

    if {[llength $args] == 0} {
        ## If no arguments, returns the path the alias points to
        return $w
    }
    set command [lindex $args 0]
    set args [lrange $args 1 end]
    switch -- [string tolower $command] {
        "setvar" {
            foreach {varname value} $args {}
            if {$value == ""} {
                return [set ::${w}::${varname}]
            } else {
                return [set ::${w}::${varname} $value]
            }
        }
        "hide" - "show" {
            Window [string tolower $command] $w
        }
        "showmodal" {
            ## modal dialog ends when window is destroyed
            Window show $w; raise $w
            grab $w; tkwait window $w; grab release $w
        }
        "startmodal" {
            ## ends when endmodal called
            Window show $w; raise $w
            set ::${w}::_modal 1
            grab $w; tkwait variable ::${w}::_modal; grab release $w
        }
        "endmodal" {
            ## ends modal dialog started with startmodal, argument is var name
            set ::${w}::_modal 0
            Window hide $w
        }
        default {
            uplevel $w $command $args
        }
    }
}
#############################################################################
## Library Procedure:  vTcl:WidgetProc

proc ::vTcl:WidgetProc {w args} {
    ## This procedure may be used free of restrictions.
    ##    Exception added by Christian Gavin on 08/08/02.
    ## Other packages and widget toolkits have different licensing requirements.
    ##    Please read their license agreements for details.

    if {[llength $args] == 0} {
        ## If no arguments, returns the path the alias points to
        return $w
    }

    set command [lindex $args 0]
    set args [lrange $args 1 end]
    uplevel $w $command $args
}
#############################################################################
## Library Procedure:  vTcl:toplevel

proc ::vTcl:toplevel {args} {
    ## This procedure may be used free of restrictions.
    ##    Exception added by Christian Gavin on 08/08/02.
    ## Other packages and widget toolkits have different licensing requirements.
    ##    Please read their license agreements for details.
    uplevel #0 eval toplevel $args
    set target [lindex $args 0]
    namespace eval ::$target {set _modal 0}
}
}


if {[info exists vTcl(sourcing)]} {

proc vTcl:project:info {} {
    set base .top33
    namespace eval ::widgets::$base {
        set set,origin 1
        set set,size 1
        set runvisible 1
    }
    namespace eval ::widgets_bindings {
        set tagslist _TopLevel
    }
    namespace eval ::vTcl::modules::main {
        set procs {
        }
        set compounds {
        }
        set projectType single
    }
}
}

#################################
# USER DEFINED PROCEDURES
#

#################################
# VTCL GENERATED GUI PROCEDURES
#

proc vTclWindow. {base} {
    if {$base == ""} {
        set base .
    }
    ###################
    # CREATING WIDGETS
    ###################
    wm focusmodel $top passive
    wm geometry $top 200x200+25+25; update
    wm maxsize $top 1684 1032
    wm minsize $top 116 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm withdraw $top
    wm title $top "page"
    bindtags $top "$top Page all"
    vTcl:FireEvent $top <<Create>>
    wm protocol $top WM_DELETE_WINDOW "vTcl:FireEvent $top <<DeleteWindow>>"

    ###################
    # SETTING GEOMETRY
    ###################

    vTcl:FireEvent $base <<Ready>>
}

proc vTclWindow.top33 {base} {
    if {$base == ""} {
        set base .top33
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl:toplevel $top -class Toplevel
    wm focusmodel $top passive
    wm geometry $top 600x450+513+198; update
    wm maxsize $top 1684 1032
    wm minsize $top 116 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "New Toplevel 1"
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    bindtags $top "$top Toplevel all _TopLevel"
    vTcl:FireEvent $top <<Create>>
    wm protocol $top WM_DELETE_WINDOW "vTcl:FireEvent $top <<DeleteWindow>>"

    label $top.lab34 \
        -text {KBotics Scouting} 
    vTcl:DefineAlias "$top.lab34" "Title" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab35 \
        -text {version 0.1} 
    vTcl:DefineAlias "$top.lab35" "version" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab36 \
        \
        -text {(C) Russell Dawes, Sawyer Ship-Wiedersprecher, and Kevin Hughes} 
    vTcl:DefineAlias "$top.lab36" "copyright" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab37 \
        -text {Match #} 
    vTcl:DefineAlias "$top.lab37" "Match" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent38 \
        -background white 
    vTcl:DefineAlias "$top.ent38" "MatchEntry" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab39 \
        -text {Red Score} 
    vTcl:DefineAlias "$top.lab39" "RedScore" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab40 \
        -text {Blue Score} 
    vTcl:DefineAlias "$top.lab40" "BlueScore" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent41 \
        -background white 
    vTcl:DefineAlias "$top.ent41" "RedEntry" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent42 \
        -background white 
    vTcl:DefineAlias "$top.ent42" "BlueEntry" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab43 \
        -text Team 
    vTcl:DefineAlias "$top.lab43" "TeamText1" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab44 \
        -text {#} 
    vTcl:DefineAlias "$top.lab44" "hastag1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent45 \
        -background white 
    vTcl:DefineAlias "$top.ent45" "RedEntry1" vTcl:WidgetProc "Toplevel1" 1
    label $top.cpd46 \
        -text {#} 
    vTcl:DefineAlias "$top.cpd46" "hashtag2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.cpd47 \
        -background white 
    vTcl:DefineAlias "$top.cpd47" "RedEntry2" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab48 \
        -text {#} 
    vTcl:DefineAlias "$top.lab48" "hashtag3" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent49 \
        -background white 
    vTcl:DefineAlias "$top.ent49" "RedEntry3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab50 \
        -text Team 
    vTcl:DefineAlias "$top.lab50" "TeamText2" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab51 \
        -text Team 
    vTcl:DefineAlias "$top.lab51" "TeamText3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab52 \
        -text Team 
    vTcl:DefineAlias "$top.lab52" "TeamText4" vTcl:WidgetProc "Toplevel1" 1
    label $top.cpd53 \
        -text Team 
    vTcl:DefineAlias "$top.cpd53" "TeamText5" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab54 \
        -text Team 
    vTcl:DefineAlias "$top.lab54" "TeamText6" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab55 \
        -text {#} 
    vTcl:DefineAlias "$top.lab55" "hashtag4" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent56 \
        -background white 
    vTcl:DefineAlias "$top.ent56" "BlueEntry1" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab57 \
        -text {#} 
    vTcl:DefineAlias "$top.lab57" "hashtag5" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent58 \
        -background white 
    vTcl:DefineAlias "$top.ent58" "BlueEntry2" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab59 \
        -text {#} 
    vTcl:DefineAlias "$top.lab59" "hashtag6" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent60 \
        -background white 
    vTcl:DefineAlias "$top.ent60" "BlueEntry3" vTcl:WidgetProc "Toplevel1" 1
    button $top.but33 \
        -pady 0 -text Submit 
    vTcl:DefineAlias "$top.but33" "Submit" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab38 \
        -text Points 
    vTcl:DefineAlias "$top.lab38" "PointsText1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent39 \
        -background white 
    vTcl:DefineAlias "$top.ent39" "RedPoints1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent40 \
        -background white 
    vTcl:DefineAlias "$top.ent40" "RedPoints2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent43 \
        -background white 
    vTcl:DefineAlias "$top.ent43" "RedPoints3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab45 \
        -text Shots 
    vTcl:DefineAlias "$top.lab45" "ShotsText1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent46 \
        -background white 
    vTcl:DefineAlias "$top.ent46" "RedShots1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent47 \
        -background white 
    vTcl:DefineAlias "$top.ent47" "RedShots2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent48 \
        -background white 
    vTcl:DefineAlias "$top.ent48" "RedShots3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab49 \
        -text Height 
    vTcl:DefineAlias "$top.lab49" "HeightText1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent50 \
        -background white 
    vTcl:DefineAlias "$top.ent50" "RedHeight1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent51 \
        -background white 
    vTcl:DefineAlias "$top.ent51" "RedHeight2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent52 \
        -background white 
    vTcl:DefineAlias "$top.ent52" "RedHeight3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab53 \
        -text Points 
    vTcl:DefineAlias "$top.lab53" "PointsText2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent54 \
        -background white 
    vTcl:DefineAlias "$top.ent54" "BluePoints1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent55 \
        -background white 
    vTcl:DefineAlias "$top.ent55" "BluePoints2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent57 \
        -background white 
    vTcl:DefineAlias "$top.ent57" "Entry21" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab58 \
        -text Shots 
    vTcl:DefineAlias "$top.lab58" "ShotsText2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent59 \
        -background white 
    vTcl:DefineAlias "$top.ent59" "BlueShots1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent61 \
        -background white 
    vTcl:DefineAlias "$top.ent61" "BlueShots2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent62 \
        -background white 
    vTcl:DefineAlias "$top.ent62" "BlueShots3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab63 \
        -text Height 
    vTcl:DefineAlias "$top.lab63" "HeightText2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent64 \
        -background white 
    vTcl:DefineAlias "$top.ent64" "BlueHeight1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent65 \
        -background white 
    vTcl:DefineAlias "$top.ent65" "BlueHeight2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent66 \
        -background white 
    vTcl:DefineAlias "$top.ent66" "BlueHeight3" vTcl:WidgetProc "Toplevel1" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.lab34 \
        -in $top -x 230 -y -10 -width 111 -height 51 -anchor nw \
        -bordermode ignore 
    place $top.lab35 \
        -in $top -x 250 -y 30 -width 71 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab36 \
        -in $top -x 100 -y 50 -width 371 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab37 \
        -in $top -x 210 -y 100 -anchor nw -bordermode ignore 
    place $top.ent38 \
        -in $top -x 270 -y 100 -anchor nw -bordermode ignore 
    place $top.lab39 \
        -in $top -x 60 -y 140 -width 71 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab40 \
        -in $top -x 460 -y 140 -width 71 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.ent41 \
        -in $top -x 40 -y 170 -anchor nw -bordermode ignore 
    place $top.ent42 \
        -in $top -x 440 -y 170 -anchor nw -bordermode ignore 
    place $top.lab43 \
        -in $top -x 60 -y 230 -anchor nw -bordermode ignore 
    place $top.lab44 \
        -in $top -x 30 -y 260 -anchor nw -bordermode ignore 
    place $top.ent45 \
        -in $top -x 50 -y 260 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.cpd46 \
        -in $top -x 110 -y 260 -anchor nw -bordermode inside 
    place $top.cpd47 \
        -in $top -x 130 -y 260 -width 54 -height 19 -anchor nw \
        -bordermode inside 
    place $top.lab48 \
        -in $top -x 190 -y 260 -anchor nw -bordermode ignore 
    place $top.ent49 \
        -in $top -x 210 -y 260 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab50 \
        -in $top -x 140 -y 230 -anchor nw -bordermode ignore 
    place $top.lab51 \
        -in $top -x 220 -y 230 -anchor nw -bordermode ignore 
    place $top.lab52 \
        -in $top -x 370 -y 230 -anchor nw -bordermode ignore 
    place $top.cpd53 \
        -in $top -x 430 -y 230 -width 56 -height 21 -anchor nw \
        -bordermode inside 
    place $top.lab54 \
        -in $top -x 510 -y 230 -anchor nw -bordermode ignore 
    place $top.lab55 \
        -in $top -x 340 -y 260 -anchor nw -bordermode ignore 
    place $top.ent56 \
        -in $top -x 360 -y 260 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab57 \
        -in $top -x 420 -y 260 -anchor nw -bordermode ignore 
    place $top.ent58 \
        -in $top -x 440 -y 260 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab59 \
        -in $top -x 500 -y 260 -anchor nw -bordermode ignore 
    place $top.ent60 \
        -in $top -x 520 -y 260 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.but33 \
        -in $top -x 230 -y 390 -width 147 -height 54 -anchor nw \
        -bordermode ignore 
    place $top.lab38 \
        -in $top -x 10 -y 300 -width 31 -height 11 -anchor nw \
        -bordermode ignore 
    place $top.ent39 \
        -in $top -x 50 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent40 \
        -in $top -x 130 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent43 \
        -in $top -x 210 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab45 \
        -in $top -x 10 -y 330 -width 31 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.ent46 \
        -in $top -x 50 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent47 \
        -in $top -x 130 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent48 \
        -in $top -x 210 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab49 \
        -in $top -x 0 -y 360 -anchor nw -bordermode ignore 
    place $top.ent50 \
        -in $top -x 50 -y 360 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent51 \
        -in $top -x 130 -y 360 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent52 \
        -in $top -x 210 -y 360 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab53 \
        -in $top -x 320 -y 300 -anchor nw -bordermode ignore 
    place $top.ent54 \
        -in $top -x 360 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent55 \
        -in $top -x 440 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent57 \
        -in $top -x 520 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab58 \
        -in $top -x 320 -y 330 -anchor nw -bordermode ignore 
    place $top.ent59 \
        -in $top -x 360 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent61 \
        -in $top -x 440 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent62 \
        -in $top -x 520 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab63 \
        -in $top -x 310 -y 360 -anchor nw -bordermode ignore 
    place $top.ent64 \
        -in $top -x 360 -y 360 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent65 \
        -in $top -x 440 -y 360 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent66 \
        -in $top -x 520 -y 360 -width 54 -height 19 -anchor nw \
        -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

#############################################################################
## Binding tag:  _TopLevel

bind "_TopLevel" <<Create>> {
    if {![info exists _topcount]} {set _topcount 0}; incr _topcount
}
bind "_TopLevel" <<DeleteWindow>> {
    if {[set ::%W::_modal]} {
                vTcl:Toplevel:WidgetProc %W endmodal
            } else {
                destroy %W; if {$_topcount == 0} {exit}
            }
}
bind "_TopLevel" <Destroy> {
    if {[winfo toplevel %W] == "%W"} {incr _topcount -1}
}

Window show .
Window show .top33

