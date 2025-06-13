package com.ruoyi.userSys.controller;

import java.util.List;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.log.annotation.Log;
import com.ruoyi.common.log.enums.BusinessType;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.userSys.domain.SysUser;
import com.ruoyi.userSys.service.ISysUserService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 用户信息Controller
 * 
 * @author ruoyi
 * @date 2024-07-06
 */
@RestController
@RequestMapping("/userSys")
public class SysUserController extends BaseController
{
    @Autowired
    private ISysUserService sysUserService;

    /**
     * 查询用户信息列表
     */
    @RequiresPermissions("userSys:userSys:list")
    @GetMapping("/list")
    public TableDataInfo list(SysUser sysUser)
    {
        startPage();
        List<SysUser> list = sysUserService.selectSysUserList(sysUser);
        return getDataTable(list);
    }

    /**
     * 导出用户信息列表
     */
    @RequiresPermissions("userSys:userSys:export")
    @Log(title = "用户信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, SysUser sysUser)
    {
        List<SysUser> list = sysUserService.selectSysUserList(sysUser);
        ExcelUtil<SysUser> util = new ExcelUtil<SysUser>(SysUser.class);
        util.exportExcel(response, list, "用户信息数据");
    }

    /**
     * 获取用户信息详细信息
     */
    @RequiresPermissions("userSys:userSys:query")
    @GetMapping(value = "/{userId}")
    public AjaxResult getInfo(@PathVariable("userId") Long userId)
    {
        return success(sysUserService.selectSysUserByUserId(userId));
    }

    /**
     * 新增用户信息
     */
    @RequiresPermissions("userSys:userSys:add")
    @Log(title = "用户信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody SysUser sysUser)
    {
        return toAjax(sysUserService.insertSysUser(sysUser));
    }

    /**
     * 修改用户信息
     */
    @RequiresPermissions("userSys:userSys:edit")
    @Log(title = "用户信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody SysUser sysUser)
    {
        return toAjax(sysUserService.updateSysUser(sysUser));
    }

    /**
     * 删除用户信息
     */
    @RequiresPermissions("userSys:userSys:remove")
    @Log(title = "用户信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{userIds}")
    public AjaxResult remove(@PathVariable Long[] userIds)
    {
        return toAjax(sysUserService.deleteSysUserByUserIds(userIds));
    }
}
