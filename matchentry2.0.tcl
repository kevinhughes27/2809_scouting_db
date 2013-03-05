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


#############################################################################
# vTcl Code to Load Stock Fonts


if {![info exist vTcl(sourcing)]} {
set vTcl(fonts,counter) 0
#############################################################################
## Procedure:  vTcl:font:add_font

proc ::vTcl:font:add_font {font_descr font_type {newkey {}}} {
    ## This procedure may be used free of restrictions.
    ##    Exception added by Christian Gavin on 08/08/02.
    ## Other packages and widget toolkits have different licensing requirements.
    ##    Please read their license agreements for details.

    if {[info exists ::vTcl(fonts,$font_descr,object)]} {
        ## cool, it already exists
        return $::vTcl(fonts,$font_descr,object)
    }

     incr ::vTcl(fonts,counter)
     set newfont [eval font create $font_descr]
     lappend ::vTcl(fonts,objects) $newfont

     ## each font has its unique key so that when a project is
     ## reloaded, the key is used to find the font description
     if {$newkey == ""} {
          set newkey vTcl:font$::vTcl(fonts,counter)

          ## let's find an unused font key
          while {[vTcl:font:get_font $newkey] != ""} {
             incr ::vTcl(fonts,counter)
             set newkey vTcl:font$::vTcl(fonts,counter)
          }
     }

     set ::vTcl(fonts,$newfont,type)       $font_type
     set ::vTcl(fonts,$newfont,key)        $newkey
     set ::vTcl(fonts,$newfont,font_descr) $font_descr
     set ::vTcl(fonts,$font_descr,object)  $newfont
     set ::vTcl(fonts,$newkey,object)      $newfont

     lappend ::vTcl(fonts,$font_type) $newfont

     ## in case caller needs it
     return $newfont
}

#############################################################################
## Procedure:  vTcl:font:getFontFromDescr

proc ::vTcl:font:getFontFromDescr {font_descr} {
    ## This procedure may be used free of restrictions.
    ##    Exception added by Christian Gavin on 08/08/02.
    ## Other packages and widget toolkits have different licensing requirements.
    ##    Please read their license agreements for details.

    if {[info exists ::vTcl(fonts,$font_descr,object)]} {
        return $::vTcl(fonts,$font_descr,object)
    } else {
        return ""
    }
}

}
#############################################################################
# vTcl Code to Load User Fonts

vTcl:font:add_font \
    "-family Arial -size 10 -weight normal -slant roman -underline 0 -overstrike 0" \
    user \
    vTcl:font11
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
    wm geometry $top 200x200+75+75; update
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
    vTcl:toplevel $top -class Toplevel \
        -menu "$top.m39" 
    wm withdraw $top
    wm focusmodel $top passive
    wm geometry $top 1167x759+321+95; update
    wm maxsize $top 1684 1032
    wm minsize $top 116 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm title $top "New Toplevel 1"
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    bindtags $top "$top Toplevel all _TopLevel"
    vTcl:FireEvent $top <<Create>>
    wm protocol $top WM_DELETE_WINDOW "vTcl:FireEvent $top <<DeleteWindow>>"

    label $top.lab34 \
        -activebackground {#ffffff} -activeforeground {#000000} \
        -background {#000000} \
        -font [vTcl:font:getFontFromDescr "-family Arial -size 10 -weight normal -slant roman -underline 0 -overstrike 0"] \
        -foreground {#ffffff} -text {KBotics Scouting} 
    vTcl:DefineAlias "$top.lab34" "Title" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab35 \
        -activebackground {#000000} -activeforeground {#ffffff} \
        -background {#000000} -foreground {#ffffff} -text {version BETA 0.2} 
    vTcl:DefineAlias "$top.lab35" "version" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab36 \
        -background {#000000} -foreground {#ffffff} \
        -text {(C) Russell Dawes, Sawyer Ship-Wiedersprecher, and Kevin Hughes} 
    vTcl:DefineAlias "$top.lab36" "copyright" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab37 \
        -background {#000000} -foreground {#ffffff} -text {Match #} 
    vTcl:DefineAlias "$top.lab37" "Match" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent38 \
        -background white 
    vTcl:DefineAlias "$top.ent38" "MatchEntry" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab39 \
        -background {#000000} -foreground {#ffffff} -text {Red Team} 
    vTcl:DefineAlias "$top.lab39" "RedTeam" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab40 \
        -background {#000000} -foreground {#ffffff} -text {Blue Team} 
    vTcl:DefineAlias "$top.lab40" "BlueTeam" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab43 \
        -activebackground {#000000} -background {#ff0000} -text Team 
    vTcl:DefineAlias "$top.lab43" "TeamText1" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab44 \
        -background {#ff0000} -text {#} 
    vTcl:DefineAlias "$top.lab44" "hastag1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent45 \
        -background white 
    vTcl:DefineAlias "$top.ent45" "RedEntry1" vTcl:WidgetProc "Toplevel1" 1
    label $top.cpd46 \
        -background {#ff0000} -text {#} 
    vTcl:DefineAlias "$top.cpd46" "hashtag2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.cpd47 \
        -background white 
    vTcl:DefineAlias "$top.cpd47" "RedEntry2" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab48 \
        -background {#ff0000} -text {#} 
    vTcl:DefineAlias "$top.lab48" "hashtag3" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent49 \
        -background white 
    vTcl:DefineAlias "$top.ent49" "RedEntry3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab50 \
        -background {#ff0000} -text Team 
    vTcl:DefineAlias "$top.lab50" "TeamText2" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab51 \
        -background {#ff0000} -text Team 
    vTcl:DefineAlias "$top.lab51" "TeamText3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab52 \
        -background {#0000ff} -text Team 
    vTcl:DefineAlias "$top.lab52" "TeamText4" vTcl:WidgetProc "Toplevel1" 1
    label $top.cpd53 \
        -background {#0000ff} -text Team 
    vTcl:DefineAlias "$top.cpd53" "TeamText5" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab54 \
        -background {#0000ff} -text Team 
    vTcl:DefineAlias "$top.lab54" "TeamText6" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab55 \
        -background {#0000ff} -text {#} 
    vTcl:DefineAlias "$top.lab55" "hashtag4" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent56 \
        -background white 
    vTcl:DefineAlias "$top.ent56" "BlueEntry1" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab57 \
        -background {#0000ff} -text {#} 
    vTcl:DefineAlias "$top.lab57" "hashtag5" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent58 \
        -background white 
    vTcl:DefineAlias "$top.ent58" "BlueEntry2" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab59 \
        -background {#0000ff} -text {#} 
    vTcl:DefineAlias "$top.lab59" "hashtag6" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent60 \
        -background white 
    vTcl:DefineAlias "$top.ent60" "BlueEntry3" vTcl:WidgetProc "Toplevel1" 1
    button $top.but33 \
        -pady 0 -text Submit 
    vTcl:DefineAlias "$top.but33" "Submit" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab38 \
        -background {#ff0000} -text Auto 
    vTcl:DefineAlias "$top.lab38" "PointsText1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent39 \
        -background white 
    vTcl:DefineAlias "$top.ent39" "RedAuto1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent40 \
        -background white 
    vTcl:DefineAlias "$top.ent40" "RedAuto2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent43 \
        -background white 
    vTcl:DefineAlias "$top.ent43" "RedAuto3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab45 \
        -background {#ff0000} -text {3 pointers} 
    vTcl:DefineAlias "$top.lab45" "ShotsText1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent46 \
        -background white 
    vTcl:DefineAlias "$top.ent46" "Red3Points1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent47 \
        -background white 
    vTcl:DefineAlias "$top.ent47" "Red3Points2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent48 \
        -background white 
    vTcl:DefineAlias "$top.ent48" "Red3Points3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab49 \
        -background {#ff0000} -text {2 pointers} 
    vTcl:DefineAlias "$top.lab49" "HeightText1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent50 \
        -background white 
    vTcl:DefineAlias "$top.ent50" "Red2Points1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent51 \
        -background white 
    vTcl:DefineAlias "$top.ent51" "Red2Points2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent52 \
        -background white 
    vTcl:DefineAlias "$top.ent52" "Red2Points3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab53 \
        -background {#0000ff} -text Auto 
    vTcl:DefineAlias "$top.lab53" "PointsText2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent54 \
        -background white 
    vTcl:DefineAlias "$top.ent54" "BlueAuto1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent55 \
        -background white 
    vTcl:DefineAlias "$top.ent55" "BlueAuto2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent57 \
        -background white 
    vTcl:DefineAlias "$top.ent57" "BlueAuto3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab58 \
        -background {#0000ff} -text {3 pointers} 
    vTcl:DefineAlias "$top.lab58" "ShotsText2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent59 \
        -background white 
    vTcl:DefineAlias "$top.ent59" "Blue3Points1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent61 \
        -background white 
    vTcl:DefineAlias "$top.ent61" "Blue3Points2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent62 \
        -background white 
    vTcl:DefineAlias "$top.ent62" "Blue3Points3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab63 \
        -background {#0000ff} -text {2 pointers} 
    vTcl:DefineAlias "$top.lab63" "HeightText2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent64 \
        -background white 
    vTcl:DefineAlias "$top.ent64" "Blue2Points1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent65 \
        -background white 
    vTcl:DefineAlias "$top.ent65" "Blue2Points2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent66 \
        -background white 
    vTcl:DefineAlias "$top.ent66" "Blue2Points3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab33 \
        -background {#ff0000} -text {1 pointers} 
    vTcl:DefineAlias "$top.lab33" "Label1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent34 \
        -background white 
    vTcl:DefineAlias "$top.ent34" "Red1Points1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent35 \
        -background white 
    vTcl:DefineAlias "$top.ent35" "Red1Points2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent36 \
        -background white 
    vTcl:DefineAlias "$top.ent36" "Red1Points3" vTcl:WidgetProc "Toplevel1" 1
    label $top.cpd37 \
        -background {#0000ff} -text {1 pointers} 
    vTcl:DefineAlias "$top.cpd37" "Label2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent41 \
        -background white 
    vTcl:DefineAlias "$top.ent41" "Blue1Points1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent42 \
        -background white 
    vTcl:DefineAlias "$top.ent42" "Blue1Points2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent44 \
        -background white 
    vTcl:DefineAlias "$top.ent44" "Blue1Points3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab46 \
        -background {#ff0000} -text {Climb height} 
    vTcl:DefineAlias "$top.lab46" "Label3" vTcl:WidgetProc "Toplevel1" 1
    label $top.cpd59 \
        -background {#0000ff} -text {Climb height} 
    vTcl:DefineAlias "$top.cpd59" "Label4" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab69 \
        -text Notes 
    vTcl:DefineAlias "$top.lab69" "Label5" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab77 \
        -background {#ff0000} -text {Red Total Score} 
    vTcl:DefineAlias "$top.lab77" "Label6" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent78 \
        -background white 
    vTcl:DefineAlias "$top.ent78" "RedScore1" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab79 \
        -background {#0000ff} -text {Blue Total Score} 
    vTcl:DefineAlias "$top.lab79" "Label7" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent80 \
        -background white 
    vTcl:DefineAlias "$top.ent80" "BlueScore1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent81 \
        -background white 
    vTcl:DefineAlias "$top.ent81" "RedClimbHeight1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent82 \
        -background white 
    vTcl:DefineAlias "$top.ent82" "RedClimbHeight2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent83 \
        -background white 
    vTcl:DefineAlias "$top.ent83" "RedClimbHeight3" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent84 \
        -background white 
    vTcl:DefineAlias "$top.ent84" "BlueClimbHeight1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent85 \
        -background white 
    vTcl:DefineAlias "$top.ent85" "BlueClimbHeight2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent86 \
        -background white 
    vTcl:DefineAlias "$top.ent86" "BlueClimbHeight3" vTcl:WidgetProc "Toplevel1" 1
    canvas $top.can37 \
        -background Blue -borderwidth 2 -closeenough 1.0 -height 782 \
        -relief ridge -width 606 
    vTcl:DefineAlias "$top.can37" "Canvas1" vTcl:WidgetProc "Toplevel1" 1
    menu $top.m39 \
        -activebackground SystemHighlight \
        -activeforeground SystemHighlightText -background {#d9d9d9} \
        -font {{MS Sans Serif} 10} -tearoff 0 
    canvas $top.cpd43 \
        -background Red -borderwidth 2 -closeenough 1.0 -height 782 \
        -relief ridge -width 606 
    vTcl:DefineAlias "$top.cpd43" "Canvas2" vTcl:WidgetProc "Toplevel1" 1
    canvas $top.cpd45 \
        -background Black -borderwidth 2 -closeenough 1.0 -height 130 \
        -relief ridge -width 1194 
    vTcl:DefineAlias "$top.cpd45" "Canvas3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab41 \
        -background {#ff0000} -text {5 pointers} 
    vTcl:DefineAlias "$top.lab41" "5Points1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent53 \
        -background white 
    vTcl:DefineAlias "$top.ent53" "Red5Points1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent63 \
        -background white 
    vTcl:DefineAlias "$top.ent63" "Red5Points2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent67 \
        -background white 
    vTcl:DefineAlias "$top.ent67" "Red5Points3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab68 \
        -background {#0000ff} -text {5 Pointers} 
    vTcl:DefineAlias "$top.lab68" "5Points2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent69 \
        -background white 
    vTcl:DefineAlias "$top.ent69" "Blue5Pointers1" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent76 \
        -background white 
    vTcl:DefineAlias "$top.ent76" "Blue5Points2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent77 \
        -background white 
    vTcl:DefineAlias "$top.ent77" "Blue5Points3" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex34 \
        -background white -height 10 -width 20 -wrap none 
    vTcl:DefineAlias "$top.tex34" "RedNote1" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex35 \
        -background white -height 164 -width 164 -wrap none 
    vTcl:DefineAlias "$top.tex35" "Text2" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex36 \
        -background white -height 10 -width 20 -wrap none 
    vTcl:DefineAlias "$top.tex36" "Text3" vTcl:WidgetProc "Toplevel1" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.lab34 \
        -in $top -x 510 -y 10 -width 111 -height 51 -anchor nw \
        -bordermode ignore 
    place $top.lab35 \
        -in $top -x 520 -y 40 -width 91 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab36 \
        -in $top -x 390 -y 60 -width 371 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab37 \
        -in $top -x 550 -y 80 -anchor nw -bordermode ignore 
    place $top.ent38 \
        -in $top -x 510 -y 110 -anchor nw -bordermode ignore 
    place $top.lab39 \
        -in $top -x 210 -y 100 -width 71 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab40 \
        -in $top -x 890 -y 100 -width 71 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab43 \
        -in $top -x 30 -y 150 -anchor nw -bordermode ignore 
    place $top.lab44 \
        -in $top -x 70 -y 150 -anchor nw -bordermode ignore 
    place $top.ent45 \
        -in $top -x 90 -y 150 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.cpd46 \
        -in $top -x 200 -y 150 -anchor nw -bordermode inside 
    place $top.cpd47 \
        -in $top -x 220 -y 150 -width 54 -height 19 -anchor nw \
        -bordermode inside 
    place $top.lab48 \
        -in $top -x 340 -y 150 -anchor nw -bordermode ignore 
    place $top.ent49 \
        -in $top -x 360 -y 150 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab50 \
        -in $top -x 160 -y 150 -anchor nw -bordermode ignore 
    place $top.lab51 \
        -in $top -x 300 -y 150 -anchor nw -bordermode ignore 
    place $top.lab52 \
        -in $top -x 750 -y 150 -anchor nw -bordermode ignore 
    place $top.cpd53 \
        -in $top -x 880 -y 150 -width 36 -height 21 -anchor nw \
        -bordermode inside 
    place $top.lab54 \
        -in $top -x 1010 -y 150 -anchor nw -bordermode ignore 
    place $top.lab55 \
        -in $top -x 785 -y 150 -width 13 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.ent56 \
        -in $top -x 810 -y 150 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab57 \
        -in $top -x 920 -y 150 -anchor nw -bordermode ignore 
    place $top.ent58 \
        -in $top -x 940 -y 150 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab59 \
        -in $top -x 1045 -y 150 -width 13 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.ent60 \
        -in $top -x 1060 -y 150 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.but33 \
        -in $top -x 0 -y 690 -width 1177 -height 74 -anchor nw \
        -bordermode ignore 
    place $top.lab38 \
        -in $top -x 40 -y 185 -width 31 -height 11 -anchor nw \
        -bordermode ignore 
    place $top.ent39 \
        -in $top -x 90 -y 180 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent40 \
        -in $top -x 220 -y 180 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent43 \
        -in $top -x 360 -y 180 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab45 \
        -in $top -x 10 -y 210 -width 71 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.ent46 \
        -in $top -x 90 -y 210 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent47 \
        -in $top -x 220 -y 210 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent48 \
        -in $top -x 360 -y 210 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab49 \
        -in $top -x 17 -y 240 -width 58 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.ent50 \
        -in $top -x 90 -y 240 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent51 \
        -in $top -x 220 -y 240 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent52 \
        -in $top -x 360 -y 240 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab53 \
        -in $top -x 760 -y 180 -width 32 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.ent54 \
        -in $top -x 810 -y 180 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent55 \
        -in $top -x 940 -y 180 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent57 \
        -in $top -x 1060 -y 180 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab58 \
        -in $top -x 740 -y 210 -anchor nw -bordermode ignore 
    place $top.ent59 \
        -in $top -x 810 -y 210 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent61 \
        -in $top -x 940 -y 210 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent62 \
        -in $top -x 1060 -y 210 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab63 \
        -in $top -x 740 -y 240 -anchor nw -bordermode ignore 
    place $top.ent64 \
        -in $top -x 810 -y 240 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent65 \
        -in $top -x 940 -y 240 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent66 \
        -in $top -x 1060 -y 240 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab33 \
        -in $top -x 16 -y 270 -width 58 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.ent34 \
        -in $top -x 90 -y 270 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent35 \
        -in $top -x 220 -y 270 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent36 \
        -in $top -x 360 -y 270 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.cpd37 \
        -in $top -x 740 -y 270 -anchor nw -bordermode inside 
    place $top.ent41 \
        -in $top -x 810 -y 270 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent42 \
        -in $top -x 940 -y 270 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent44 \
        -in $top -x 1060 -y 270 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab46 \
        -in $top -x 10 -y 330 -anchor nw -bordermode ignore 
    place $top.cpd59 \
        -in $top -x 730 -y 330 -anchor nw -bordermode inside 
    place $top.lab69 \
        -in $top -x 553 -y 380 -width 37 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab77 \
        -in $top -x 200 -y 360 -anchor nw -bordermode ignore 
    place $top.ent78 \
        -in $top -x 180 -y 380 -anchor nw -bordermode ignore 
    place $top.lab79 \
        -in $top -x 880 -y 360 -anchor nw -bordermode ignore 
    place $top.ent80 \
        -in $top -x 860 -y 380 -anchor nw -bordermode ignore 
    place $top.ent81 \
        -in $top -x 90 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent82 \
        -in $top -x 220 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent83 \
        -in $top -x 360 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent84 \
        -in $top -x 810 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent85 \
        -in $top -x 940 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent86 \
        -in $top -x 1060 -y 330 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.can37 \
        -in $top -x 630 -y 760 -width 606 -height 782 -anchor nw \
        -bordermode ignore 
    place $top.cpd43 \
        -in $top -x -30 -y 770 -width 614 -height 790 -anchor nw \
        -bordermode ignore 
    place $top.cpd45 \
        -in $top -x -10 -y 730 -width 1194 -height 130 -anchor nw \
        -bordermode inside 
    place $top.lab41 \
        -in $top -x 20 -y 300 -anchor nw -bordermode ignore 
    place $top.ent53 \
        -in $top -x 90 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent63 \
        -in $top -x 220 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent67 \
        -in $top -x 360 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.lab68 \
        -in $top -x 740 -y 300 -anchor nw -bordermode ignore 
    place $top.ent69 \
        -in $top -x 810 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent76 \
        -in $top -x 940 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.ent77 \
        -in $top -x 1060 -y 300 -width 54 -height 19 -anchor nw \
        -bordermode ignore 
    place $top.tex34 \
        -in $top -x 10 -y 450 -anchor nw -bordermode ignore 
    place $top.tex35 \
        -in $top -x 200 -y 450 -width 164 -height 164 -anchor nw \
        -bordermode ignore 
    place $top.tex36 \
        -in $top -x 390 -y 450 -anchor nw -bordermode ignore 

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
